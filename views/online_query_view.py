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
    folder = f"query_data/online_queres/{dataset}"
    results = {}
    for file in os.listdir(folder):
        system = file.split(".")[0]
        # format is 34.75137948989868 , 5.527973488013321  , q1 , 3 , 1 , day , 10000
        with open(f"{folder}/{file}", "r") as f:
            for line in open(f"{folder}/{file}"):
                runtime, var, query, n_s, n_st, time_range, batch_size = line.split(",")
                query = query.strip()
                if query == q_n and n_s == ingestion_rate:
                    results[system] = float(runtime)
    return results


class OnlineQueryView(OfflineQueryView):
    context = {
        'title': 'Online Queries',
        'heading': 'Welcome to the Online Queries Page',
        'body': 'This is the body of the Offline Queries Page',
        "datasets": ["Temp1"],
        "classes": "online-query",
        # "station_ticks": [2, 4, 6, 8, 10],
        # "sensor_ticks": [1, 20, 40, 60, 80, 100],
        # "time_ticks": ["Min", "H", "D", "W", "M"]
    }
    template = loader.get_template('queries/online-queries.html')

    def post(self, request):
        entry = dict(request.POST)
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        print(data)

        parsed_entry = self.parse_entry(data[0])

        result = {INFLUX: 1, QUESTDB: 3, TIMESCALEDB: 2, MONETDB: 4, EXTREMEDB: 5, CLICKHOUSE: 6, DRUID: 7}
        result = {"data": {"Online Query": result}}

        # return json respone
        return JsonResponse(result)
