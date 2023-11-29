##offlien query view

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.loader import render_to_string
from django.views import View
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
    }
    template = loader.get_template('queries/queries.html')

    def get(self, request):
        import random
        random.seed(1)
        template = loader.get_template('queries/queries.html')

        self.context["query_frame"] = render_to_string('queries/query-box.html', {})
        self.context["time_stamps"] = random.sample(time_stamps_options * 100, 100)
        return HttpResponse(self.template.render(self.context, request))

    def parse_entry(self, entry):
        return {
            "query": entry["query"],
            "n_s": int(entry["sensors"]),
            "n_st": int(entry["stations"]),
            "rangeUnit": entry["time"],
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
            result["data"][f"Q{i}"] = {INFLUX: 10, QUESTDB: 3, TIMESCALEDB: 2, MONETDB: 4, EXTREMEDB: 5, CLICKHOUSE: 6,
                                       DRUID: 7}

        return JsonResponse(result)


class OnlineQueryView(OfflineQueryView):
    context = {
        'title': 'Online Queries',
        'heading': 'Welcome to the Online Queries Page',
        'body': 'This is the body of the Offline Queries Page',
    }
    template = loader.get_template('queries/online-queries.html')

    def post(self, request):
        entry = dict(request.POST)
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        parsed_entry = self.parse_entry(data[0])

        result = {INFLUX: 1, QUESTDB: 3, TIMESCALEDB: 2, MONETDB: 4, EXTREMEDB: 5, CLICKHOUSE: 6, DRUID: 7}
        result = {"data": {"Online Query": result}}

        # return json respone
        return JsonResponse(result)
