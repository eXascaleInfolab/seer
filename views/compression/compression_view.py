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
    compression_datasets = list(os.listdir("compression_data/ts"))[::-1]
    systems = ["clickhouse", "influx", "timescaledb", "druid"]
    data_cols = ['time', 's0', 's1', 's2', "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10"]

    context = {
        'title': 'Compression View',
        "compression_datasets": compression_datasets,
        'features': [("scarsity", "Missing Values"), ("outliers", "Outliers"), ("repeats", "Repeats"),
                     ("delta", "Mean Delta")]
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

        compression_data_folder = f"{self.compression_data_folder}/ts/{dataset}"
        compression_data_folder_ts = f"{self.compression_data_folder}/ts/{dataset}/{feature}"

        system_compressions = load_systems_compression(dataset)

        n_lines = 5000

        data = {}
        initial_df = pd.read_csv(f"{compression_data_folder}/original.csv", usecols=self.data_cols + ["id_station"],
                                 skiprows=lambda x: x > n_lines or x == 1)

        initial_df = initial_df[initial_df["id_station"] == initial_df["id_station"][1]]
        initial_df = initial_df.drop(columns=["id_station"])

        initial_data_set_result = {}
        for col in self.data_cols:
            initial_data_set_result[col] = initial_df[col].values.tolist()

        for file in os.listdir(compression_data_folder_ts):
            level = f"{file}".replace(".csv", "")
            data[level] = {}

            print("reading", file)
            df = pd.read_csv(f"{compression_data_folder_ts}/{file}", usecols=self.data_cols + ["id_station"],
                             skiprows=lambda x: x > n_lines or x == 1)
            df = df[df["id_station"] == df["id_station"][1]]
            df = df.drop(columns=["id_station"])
            data_set_result = {}
            for col in self.data_cols:
                data_set_result[col] = df[col].values.tolist()
            data[level]["data"] = data_set_result
            # compressions
            data[level]['compression'] = {}
            for system in self.systems:
                print("system", system)
                data[level]['compression'][system] = system_compressions[system].get(level, (-1, -1))[0]

        result = {"data": data,
                  "initial_dataset": initial_data_set_result}  # data is onyl for data with features intial dataset is without freatures
        result = convert_np_values(result)

        description = "test"
        with open(f"{self.compression_data_folder}/ts/{dataset}/description.txt", "r") as file:
            description = file.read()

        result["description"] = description
        return JsonResponse(result)
