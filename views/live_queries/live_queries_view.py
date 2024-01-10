from utils.query_translator import load_query, timescaledb_query_parser, clickhouse_query_parser
from views.live_queries.system_query_maps import run_query
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
        "systems" : ["clickhouse","timescaledb","influx" , "monetdb"],
        "classes" : "live-query",
        "datasets": ["Temperature1", "Temperature2"],
        "station_ticks": [2, 4, 6, 8, 10],
        "sensor_ticks": [1, 20, 40, 60, 80, 100],
        "time_ticks": ["Min", "H", "D", "W"]
    }

    template = loader.get_template('queries/queries_live.html')

    def post(self, request):
        print("LAUNCHIGN LIVE QUERYs")
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        parsed_entry = self.parse_entry(data[0])
        system = data[0]["system"]
        q_n = parsed_entry["query"]

        n_st = parsed_entry["n_st"]
        n_s = parsed_entry["n_s"]
        rangeUnit = parsed_entry["rangeUnit"]
        rangeL = parsed_entry["rangeL"]
        random.seed(1)

        queryResult  = run_query(system, q_n, rangeL, rangeUnit, n_st, n_s, n_it=1, dataset="d1")
        query_data = queryResult.query_data



        result = {}
        result["runtime"] = queryResult.runtime
        result["query"] = queryResult.query
        result["numberOfQueries"] = len(query_data)
        result["query_results"] = query_data[:min(12, len(query_data))]
        result["system"] = system

        return JsonResponse(result)
