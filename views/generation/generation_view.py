from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

import json
import pandas as pd
import os
import subprocess

from views.generation.utils import get_dataset_info, get_datasets

host = "gan:80" if os.getenv("using_docker") else "localhost:87"

ts_multipliers = {
    "same": 1, "1x": 1, "2x": 2, "5x": 5, "10x": 5
}


##Local test
# command = f'curl "http://{host}:87/run-pretrained?seed={"temperature"}&len_ts={1000}&nb_ts={2}"'
# subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_generated_data(seed, *, len_ts, nb_ts, num_hashtables=5, nb_top=3, hash_length_percentage=3, min=0, max=10000 , selected_series=0):
    # sample command = curl "http://{host}:80/run-pretrained?seed=bafu&len_ts=10000&nb_ts=1
    len_ts = ts_multipliers[len_ts] * (max - min)
    import subprocess
    command = (f'curl "http://{host}/run-pretrained?seed={seed}&len_ts={len_ts}&nb_ts={nb_ts}'
               f'&num_hashtables={num_hashtables}'
               f'&nb_top={nb_top}'
               f'&hash_length_percentage={hash_length_percentage}'
               f'&min={min}'
               f'&max={max}'
               f'&selected_series={selected_series}"')

    print(command)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import time
    time.sleep(3)
    # Read the generated data
    df = pd.read_csv('generation/results/generated.txt')
    return df


class GenerationView(View):
    context = {  # info box as in toml https://github.com/eXascaleInfolab/TSM-Bench/blob/main/generation/config.toml
        'title': 'Generation using GAN',
        "len_ts": ["1x", "2x", "5x", "10x"],
        "len_ts_default": "2x",
        "nb_ts": [1, 2, 5, 10],  #
        "nb_ts_default": 1,
        "num_hashtables": [1, 5, 8, 10],
        "num_hashtables_default": 8,
        "nb_top": [1, 4, 10, 16, 20],
        "nb_top_default": 4,
        "hash_length_percentage": [1, 3, 5, 10, 20, 50],
        "hash_length_percentage_default": 3
    }

    template = loader.get_template('generation/generation.html')

    @property
    def data_sets(self):
        return get_datasets()

    def get(self, request, dataset):
        self.context["data_info"] = get_dataset_info(dataset)
        self.context['data_sets'] = self.data_sets
        self.context['dataset'] = dataset
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request, dataset=None):
        print(dict(request.POST))
        folder = "generation/data"

        data_set = request.POST.get('dataset')
        generate = request.POST.get('generate')
        if generate == "false":
            original_data_set_path = f"{folder}/{data_set}/original.txt"
            # return JsonResponse(data)

            df = self.load_orginal_data(original_data_set_path)
            data = [{"name":  get_dataset_info(data_set)["header"][i] ,   "data": df[col].values.tolist()} for i, col in enumerate(df.columns)]
            return JsonResponse({
                'original': data,
                'name': [dataset[1] for dataset in self.data_sets if dataset[0] == data_set][0]
            })
        else:
            len_ts = request.POST.get('len_ts')
            nb_ts = request.POST.get('nb_ts')
            num_hashtables = request.POST.get('num_hashtables')
            nb_top = request.POST.get('nb_top')
            hash_length_percentage = request.POST.get('hash_length_percentage')
            min_ = max(0, round(float(request.POST.get('min'))), 0)
            max_ = round(float(request.POST.get('max')))
            len_seed = request.POST.get('len_seed')
            selected_series = int(request.POST.get('selected-series'))

            if len_seed == "full":
                min_ = 0
                max_ = 15000

            data_df = get_generated_data(data_set, len_ts=len_ts, nb_ts=nb_ts, num_hashtables=num_hashtables,
                                         nb_top=nb_top, hash_length_percentage=hash_length_percentage, min=min_,
                                         max=max_ , selected_series=selected_series)

            generated_data = [data_df.iloc[:, i].values.tolist() for i in range(data_df.shape[1])]
            original = pd.read_csv(f"{folder}/{data_set}/original.txt").iloc[min_:max_, selected_series].values.flatten().tolist()
            return JsonResponse({
                'generated': generated_data,
                'name': [dataset[1] for dataset in self.data_sets if dataset[0] == data_set][0],
                'original': original
            })

    def load_orginal_data(self, path):
        import pandas as pd
        df = pd.read_csv(path, sep=",")
        df = df.iloc[:15000, :10]
        return df
