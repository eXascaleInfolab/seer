import os

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View
import pandas as pd
from django.db import connection
from utils.compression_loader import load_compression_data_sets, load_systems_compression
from utils.numpy_loader import NumpyEncoder, convert_np_values
import json
class CompressionView(View):
    compression_data_folder = "compression_data"
    compression_datasets = list(os.listdir("compression_data/ts"))
    systems = ["clickhouse", "influx", "druid", "timescaledb"]
    data_cols = ['time', 's0' , 's1' , 's2']

    context = {
        'title': 'Compression View',
        "compression_datasets" : compression_datasets
    }
    template = loader.get_template('compression/compression.html')

    def get(self, request):
        print("GETTING COMPRESSION VIEW")
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request):
        """
        output:
        data:  { dataset1 : { data : dataset , compression : { influx : value , clickhouse : value , ... } } ,
                 dataset1 : { data : dataset , compression : { influx : value , clickhouse : value , ... } }
        }
        """

        print("POSTING COMPRESSION VIEW")
        dataset = request.POST.get("dataset")
        feature = request.POST.get("feature")

        compression_data_folder_ts = f"{self.compression_data_folder}/ts/{dataset}/{feature}"

        system_compressions = load_systems_compression(dataset)


        data = {}
        for file in os.listdir(compression_data_folder_ts):
            level = f"{file}".replace(".csv","")
            data[level] = {}

            print("reading" , file)
            df = pd.read_csv(f"{compression_data_folder_ts}/{file}", usecols=self.data_cols)
            data_set_result = {}
            for col in self.data_cols:
                data_set_result[col] = df[col].values.tolist()
            data[level]["data"] = data_set_result
            # compressions
            data[level]['compression'] = {}
            for system in self.systems:
                print("system" , system)
                data[level]['compression'][system] = system_compressions[system][level][0]

        result = {"data": data}
        result = convert_np_values(result)

        return JsonResponse(result)
