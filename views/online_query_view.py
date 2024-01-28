import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.loader import render_to_string
from django.views import View

from djangoProject.models import QueryModel
from utils.CONSTANTS import INFLUX, QUESTDB, TIMESCALEDB, MONETDB, EXTREMEDB, CLICKHOUSE, DRUID
import json

from views.queries import OfflineQueryView


def get_query_data(q_n, ingestion_rate, dataset="d1"):
    folder = f"query_data/online_queries/{dataset}"
    results = {}
    for file in os.listdir(folder):
        system = file.split(".")[0]
        # format is 34.75137948989868 , 5.527973488013321  , q1 , 3 , 1 , day , 10000
        with open(f"{folder}/{file}", "r") as f:
            for line in open(f"{folder}/{file}"):
                runtime, var, query, n_s, n_st, time_range, batch_size = line.split(",")
                print(query, f"q{q_n}", batch_size, ingestion_rate)
                query = query.strip()
                if query == f"q{q_n}" and int(batch_size) == ingestion_rate:
                    results[system] = float(runtime)
    return results


class OnlineQueryView(OfflineQueryView):
    context = {
        'title': 'Online Queries',
        'heading': 'Welcome to the Online Queries Page',
        'body': 'This is the body of the Offline Queries Page',
        "datasets": ["Temp1"],
        "classes": "online-query",
        "systems": [INFLUX, QUESTDB, TIMESCALEDB, MONETDB, EXTREMEDB, CLICKHOUSE],
        "station_ticks": [],
        "sensor_ticks": [],
        "time_ticks": [],
        "ingestion_rates": [1, 10, 20, 50 , 100],
    }
    template = loader.get_template('queries/online-queries.html')

    def post(self, request):
        entry = dict(request.POST)
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        ingestion_rate = int(data[0]["ingestion_rate"])
        query = data[0]["query"]

        print("ingestion_rate", ingestion_rate)
        print("query", query)

        query_data = get_query_data(query,ingestion_rate*10000)

        print(query_data)

        result = {INFLUX: 100, QUESTDB: 3, TIMESCALEDB: 2, MONETDB: 4, EXTREMEDB: 5, CLICKHOUSE: 6, DRUID: 7}
        result = {"data" : {"online": result}}

        # return json respone
        return JsonResponse(result)
