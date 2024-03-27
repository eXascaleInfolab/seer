from views.live_queries.system_query_maps import run_query
from views.offline_query_view import OfflineQueryView
from django.http import JsonResponse
from django.template import loader
import json
import random
import numpy as np

old_result = None

## systems to enable in the form
ENABLED_SYSTEMS = ["clickhouse_v2" , "mongodb"]

## mesage to be displayed on the page in the info button next to the systems Label
systems_message = "Due to the limited resources of the server, we can not run all systems at the same time."


class LiveQueryView(OfflineQueryView):
    context = {
        'title': 'SEER - Live Queries',
        'heading': 'Welcome to the Live Queries Page',
        "systems" :  ENABLED_SYSTEMS,
        "classes" : "live-query",
        "datasets": ["TempLong"],
        "station_ticks": [2, 4, 6, 8, 10],
        "sensor_ticks": [1, 20, 40, 60, 80, 100],
        "time_ticks": ["Min", "H", "D", "W"],
        "ENABLED_SYSTEMS" : ENABLED_SYSTEMS,
        "systems_message" : systems_message
    }


    template = loader.get_template('queries/live_queries/queries_live.html')

    def get(self, request):
        from systems import influx
        print("launching influx")
        influx.run_system.launch()
        return super().get(request)


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



        input_dataset = "d1"
        input_system = system
        if(system == "clickhouse_v2"):
            input_system = "clickhouse"
            input_dataset = "d1_no_time"
            print("clickhouse_v2")

        print("system", system , input_system)
        print("dataset", input_dataset)
        queryResult  = run_query(input_system, q_n, rangeL, rangeUnit, n_st, n_s, n_it=query_iterations, dataset=input_dataset)
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

        #add offline query results to the output to be displayed in the table
        response =  super().post(request)
        result["offline_query_results"] = json.loads(response.content.decode('utf-8'))

        print(result["offline_query_results"])
        return JsonResponse(result)
