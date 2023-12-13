from utils.query_translator import load_query, timescaledb_query_parser, clickhouse_query_parser
from views.offline_query_view import OfflineQueryView
from django.http import JsonResponse
from django.template import loader
import json
import time
import random
from clickhouse_driver import Client

import os

old_result = None

dataset_config = {
    "d1": {
        "time_start_stop": [
            "2019-04-30T00:00:00",
            "2019-04-01T00:00:00"
        ],
        "n_stations": 10,
        "n_sensors": 100
    },
    "d2": {
        "time_start_stop": [
            "2019-04-30T00:00:00",
            "2019-04-01T00:00:00"
        ],
        "n_stations": 2000,
        "n_sensors": 100
    }

}


class LiveQueryView(OfflineQueryView):
    context = {
        'title': 'Live Queries',
        'heading': 'Welcome to the Online Queries Page',
        "systems" : ["clickhouse","timescaledb"]
    }

    template = loader.get_template('queries/queries_live.html')

    def post(self, request):
        print("LAUNCHIGN LIVE QUERYs")
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        parsed_entry = self.parse_entry(data[0])
        print(data)
        system = data[0]["system"]
        print("SYYYYYYYYYYYYYYYYYSTEM" , system)
        q_n = parsed_entry["query"]
        query_template = load_query(system, q_n)
        query_template = query_template.replace("<db>", "d1")

        n_st = parsed_entry["n_st"]
        n_s = parsed_entry["n_s"]
        rangeUnit = parsed_entry["rangeUnit"]
        rangeL = parsed_entry["rangeL"]
        random.seed(1)

        date = "2019-04-01T00:00:00"
        random_stations = ['st' + str(z) for z in random.sample(range(10), n_st)]
        random_sensors = ['s' + str(z) for z in random.sample(range(100), n_s)]

        if system == "clickhouse":
            host = "clickhouse" if os.getenv("using_docker") else "localhost"
            parsed_query = clickhouse_query_parser(query_template, date=date,
                                                    rangeUnit=rangeUnit,
                                                    rangeL=rangeL,
                                                    sensor_list=random_sensors,
                                                    station_list=random_stations)
            client = Client(host=host, port=9000)

            start = time.time()
            query_data = client.execute(parsed_query)
            runtime = (time.time() - start) * 1000
            runtime = round(runtime, 2)
            query_data = sorted(query_data, key=lambda x: x[0])

        if system == "timescaledb":
            import psycopg2
            timescaledb_host = "timescaledb" if os.getenv("using_docker") else "localhost"

            parsed_query = timescaledb_query_parser(query_template, date=date,
                                                    rangeUnit=rangeUnit,
                                                    rangeL=rangeL,
                                                    sensor_list=random_sensors,
                                                    station_list=random_stations)

            CONNECTION = f"postgres://postgres:postgres@{timescaledb_host}:5432/postgres"
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()

            start = time.time()
            cursor.execute(parsed_query)
            query_data = cursor.fetchall()
            runtime = (time.time() - start) * 1000
            runtime = round(runtime, 2)
            query_data = sorted(query_data, key=lambda x: x[0])

        result = {}
        result["runtime"] = runtime
        result["query"] = parsed_query
        result["numberOfQueries"] = len(query_data)
        result["query_results"] = query_data[:min(12, len(query_data))]
        result["system"] = system

        return JsonResponse(result)
