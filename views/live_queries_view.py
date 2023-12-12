from utils.query_translator import load_query, query_parser
from views.offline_query_view import OfflineQueryView
##offlien query view
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.loader import render_to_string
from django.views import View
from utils.CONSTANTS import INFLUX, QUESTDB, TIMESCALEDB, MONETDB, EXTREMEDB, CLICKHOUSE, DRUID
import json

from clickhouse_driver import Client

host = "clickhouse"
old_result = None


class LiveQueryView(OfflineQueryView):
    context = {
        'title': 'Live Queries',
        'heading': 'Welcome to the Online Queries Page',
        'body': 'This is the body of the Offline Queries Page',
    }
    template = loader.get_template('queries/queries_live.html')

    def post(self, request):
        print("LAUNCHIGN ONLINE QUERYs")
        entry = dict(request.POST)
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        parsed_entry = self.parse_entry(data[0])

        system = "clickhouse"

        q_n = parsed_entry["query"]
        query = load_query(system, q_n)
        print("query", query)

        parsed_entry["query"] = query
        parsed_query = query_parser(system=system, **parsed_entry)

        print("parsed" ,parsed_query)

        result = {}

        client = Client(host=host, port=9000)

        import time
        start = time.time()
        query_data = client.execute(parsed_query)
        runtime = time.time() - start
        query_data = sorted(query_data, key=lambda x: x[0])

        print("EEEE", len(query_data))

        # runtime, query, numberOfQueries, query_results
        result["runtime"] = runtime
        result["query"] = parsed_query
        result["numberOfQueries"] = len(query_data)
        result["query_results"] = query_data[:min(12, len(query_data))]

        return JsonResponse(result)
