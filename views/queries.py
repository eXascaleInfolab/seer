##offlien query view

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.loader import render_to_string
from django.views import View

from djangoProject.models import QueryModel
from utils.CONSTANTS import INFLUX, QUESTDB, TIMESCALEDB, MONETDB, EXTREMEDB, CLICKHOUSE, DRUID
import json

# Random settings
# d1 2019-03-01T00:00:00 - 2019-04-29T23:59:40 , stations st0 - st9     , sensors s0 - s99
# d2 2019-02-01T00:00:10 - 2019-02-10T23:59:50 , stations st0 - st1999 ,  sensors s0 - s99
time_stamps_options = [
    "2019-03-01T00:00:00",
    "2019-04-29T23:59:50",
]


class OfflineQueryView(View):
    context = {
        'title': 'Offline Queries',
        'heading': 'Welcome to the Offline Queries Page',
        'body': 'This is the body of the Offline Queries Page',
        "classes": "offline-query",
        "datasets": ["TempLong", "TempMulti"],
        "station_ticks": [2, 4, 6, 8, 10],
        "sensor_ticks": [1, 20, 40, 60, 80, 100],
        "time_ticks": ["Min", "H", "D", "W", "M"],
        "systems": [INFLUX, QUESTDB, TIMESCALEDB, MONETDB, EXTREMEDB, CLICKHOUSE, DRUID]
    }

    data_set_map = {
        "TempLong": "d1",
        "TempMulti": "d2"
    }

    template = loader.get_template('queries/queries.html')
    model = QueryModel

    def query_name(self, index):
        return f"Q{index + 1}"

    def get(self, request):
        import random
        random.seed(1)
        template = loader.get_template('queries/queries.html')

        self.context["query_frame"] = render_to_string('queries/query-box.html', self.context)
        self.context["time_stamps"] = random.sample(time_stamps_options * 100, 100)
        return HttpResponse(self.template.render(self.context, request))

    def parse_entry(self, entry):
        return {
            "query": entry["query"],
            "n_s": int(entry["sensors"]),
            "n_st": int(entry["stations"]),
            "rangeUnit": entry["time"].lower(),
            "dataset": entry["dataset"],
            "rangeL": 1,
        }

    def post(self, request):
        query = request.POST.get('query')
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        result = {"data": {}}
        for i, entry in enumerate(data):
            parsed_entry = self.parse_entry(entry)
            print(parsed_entry)
            print("DATSET", parsed_entry["dataset"])
            dataset =  self.data_set_map[parsed_entry["dataset"]]
            runtimes = QueryModel.get_all_system_runtimes(dataset=dataset,
                                                          query="q" + parsed_entry["query"],
                                                          n_sensors=parsed_entry["n_s"],
                                                          n_stations=parsed_entry["n_st"],
                                                          time_range=parsed_entry["rangeUnit"]
                                                          )

            result["data"][self.query_name(i)] = runtimes

        return JsonResponse(result)

