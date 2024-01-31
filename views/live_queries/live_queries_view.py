from views.live_queries.system_query_maps import run_query
from views.queries import OfflineQueryView
from django.http import JsonResponse
from django.template import loader
import json
import random
import numpy as np

old_result = None

ENABLED_SYSTEMS = ["clickhouse", "timescaledb"]

class LiveQueryView(OfflineQueryView):
    context = {
        'title': 'SEER - Live Queries',
        'heading': 'Welcome to the Online Queries Page',
        "systems" : ["clickhouse","timescaledb","influx" , "monetdb"],
        "classes" : "live-query",
        "datasets": ["TempLong"],
        "station_ticks": [2, 4, 6, 8, 10],
        "sensor_ticks": [1, 20, 40, 60, 80, 100],
        "time_ticks": ["Min", "H", "D", "W"],
        "ENABLED_SYSTEMS" : ENABLED_SYSTEMS
    }


    template = loader.get_template('queries/live_queries/queries_live.html')

    def post(self, request):
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        parsed_entry = self.parse_entry(data[0])
        system = data[0]["system"]
        query_iterations = int(data[0]["query_iterations"])
        print("query_iterations", query_iterations)
        q_n = parsed_entry["query"]

        n_st = parsed_entry["n_st"]
        n_s = parsed_entry["n_s"]
        rangeUnit = parsed_entry["rangeUnit"]
        rangeL = parsed_entry["rangeL"]
        random.seed(1)

        queryResult  = run_query(system, q_n, rangeL, rangeUnit, n_st, n_s, n_it=query_iterations, dataset="d1")
        query_data = queryResult.query_data



        result = {}
        result["runtime"] = queryResult.runtime
        result["runtimes"] = runtimes = queryResult.runtimes

        runtimes = np.array(runtimes)
        box_plot_data = [min(runtimes) ,  float(np.percentile(runtimes, 25)) ,  float(np.percentile(runtimes, 50)) ,  float(np.percentile(runtimes, 75)), max(runtimes) ]
        result["boxplot_data"] = box_plot_data


        # Determine outliers (values outside 1.5 * IQR from the quartiles)
        iqr = np.percentile(runtimes, 50)-np.percentile(runtimes, 25)
        lower_bound = np.percentile(runtimes, 25) - 1.5 * iqr
        upper_bound = np.percentile(runtimes, 75) + 1.5 * iqr
        outliers = runtimes[ (runtimes < lower_bound) | (runtimes > upper_bound)]

        result["outliers"] = outliers.tolist()
        result["label"] =  f"{system} q{q_n}"
        result["query"] = queryResult.query
        result["numberOfQueries"] = len(query_data)
        result["query_results"] = query_data[:min(12, len(query_data))]
        result["system"] = system

        return JsonResponse(result)
