from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

import json
import pandas as pd
import os

host = "gan" if os.getenv("using_docker") else "172.17.0.2"

with open('generation_data/datasets.json', 'r') as file:
    generation_datasets_info = json.load(file)

ts_multipliers = {
    "same": 1, "2x": 2, "3x": 3, "5x": 5 , "1x" : 1
}


def get_generated_data(seed, *, len_ts, nb_ts, num_hashtables=5, nb_top=3, hash_length_percentage=3, min=0, max=10000):
    # sample command = curl "http://{host}:80/run-pretrained?seed=bafu&len_ts=10000&nb_ts=1
    len_ts = ts_multipliers[len_ts]*(max-min)
    import subprocess
    command = (f'curl "http://{host}:80/run-pretrained?seed={seed}&len_ts={len_ts}&nb_ts={nb_ts}'
               f'&num_hashtables={num_hashtables}'
               f'&nb_top={nb_top}'
               f'&hash_length_percentage={hash_length_percentage}'
               f'&min={min}'
               f'&max={max}"')

    print(command)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("after run command")
    # Read the generated data
    df = pd.read_csv('generation/results/generated.txt')
    print(df)
    return df


class GenerationView(View):
    context = { #info box as in toml https://github.com/eXascaleInfolab/TSM-Bench/blob/main/generation/config.toml
        'title': 'Generation using GAN',
        "len_ts": ["1x", "2x", "3x", "5x"],
        "len_ts_default": "1x",
        "nb_ts": [1, 2, 5, 10], #
        "nb_ts_default": 5,
        "num_hashtables": [1, 5, 8, 10],
        "num_hashtables_default": 8,
        "nb_top": [1, 4, 10, 16, 20],
        "nb_top_default" : 4,
        "hash_length_percentage": [ 1, 3, 5, 10, 20, 50] ,
        "hash_length_percentage_default": 3
    }

    template = loader.get_template('generation/generation.html')
    data_sets = [("temperature", "Temperature"), ("conductivity", "Conductivity"), ("pH_accuracy", "pH_accuracy")]

    def get(self, request, dataset):
        self.context["data_info"] = generation_datasets_info[dataset]
        self.context['data_sets'] = self.data_sets
        self.context['dataset'] = dataset
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request, dataset=None):
        print(dict(request.POST))
        folder = "generation_data"

        data_set = request.POST.get('dataset')
        generate = request.POST.get('generate')
        if generate == "false":
            original_data_set_path = f"{folder}/{data_set}/original.txt"
            # return JsonResponse(data)
            return JsonResponse({
                'original': self.load_orginal_data(original_data_set_path),
                'name': [dataset[1] for dataset in self.data_sets if dataset[0] == data_set][0]
            })
        else:
            len_ts = request.POST.get('len_ts')
            nb_ts = request.POST.get('nb_ts')
            num_hashtables = request.POST.get('num_hashtables')
            nb_top = request.POST.get('nb_top')
            hash_length_percentage = request.POST.get('hash_length_percentage')
            min = round(float(request.POST.get('min')))
            max = round(float(request.POST.get('max')))

            data_df = get_generated_data(data_set, len_ts=len_ts, nb_ts=nb_ts, num_hashtables=num_hashtables,
                                         nb_top=nb_top, hash_length_percentage=hash_length_percentage, min=min, max=max)

            generated_data = [data_df.iloc[:, i].values.tolist() for i in range(data_df.shape[1])]

            original = pd.read_csv(f"{folder}/{data_set}/original.txt").iloc[min:max, 0].values.flatten().tolist()
            return JsonResponse({
                'generated': generated_data,
                'name': [dataset[1] for dataset in self.data_sets if dataset[0] == data_set][0],
                'original': original
            })

    def load_orginal_data(self, path):
        import pandas as pd
        df = pd.read_csv(path, sep=",")
        return df.values.flatten()[:15000].tolist()

    def load_generated_data(self, path, length, count):
        import pandas as pd
        df = pd.read_csv(path, sep=",")
        # return the first count columns of the df in a list
        # e.g., return [ col1_list, col2_list, ... , col_count_list]
        return [df.iloc[:, i].values.tolist() for i in range(count)]
