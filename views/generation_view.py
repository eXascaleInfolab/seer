from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

from django.db import connection
from utils.compression_loader import load_compression_data_sets, load_systems_compression
from utils.numpy_loader import NumpyEncoder
import json

class GenerationView(View):
    context = {
        'title': 'Generation using GAN',
    }
    template = loader.get_template('generation/generation.html')
    data_sets = [ ("bafu","Bafu") , ("conductivity","Conductivity") , ("pH_accuracy","pH_accuracy") ]
    generation_lengths = [2000,  5000, 20000 , 50000]
    generation_counts = [1,2,5,10]

    def get(self, request):

        self.context['data_sets'] = self.data_sets
        self.context['generation_lengths'] = self.generation_lengths
        self.context['generation_counts'] = self.generation_counts

        return HttpResponse(self.template.render(self.context, request))

    def post(self, request):
        folder = "generation_data"

        data_set = request.POST.get('dataset')
        generate = request.POST.get('generate')
        if generate == "false":
            original_data_set_path = f"{folder}/{data_set}/original.txt"
            # return JsonResponse(data)
            return JsonResponse({
                'original': self.load_orginal_data(original_data_set_path),
                'name' : [dataset[1] for dataset in self.data_sets if dataset[0] == data_set][0]
            })
        else:
            length = int(request.POST.get('generationLength'))
            count = int(request.POST.get('generationCount'))
            generated_data_set_path = f"{folder}/{data_set}/synthetic.txt"
            print("AAAAAAAAAAAAAAAAAAAAAAAAA",length, count)
            return JsonResponse({
                'generated': self.load_generated_data(generated_data_set_path, length, count),
                'name': [dataset[1] for dataset in self.data_sets if dataset[0] == data_set][0]
            })


    def load_orginal_data(self, path):
        import pandas as pd
        df = pd.read_csv(path, sep=",")
        return df.values.flatten().tolist()

    def load_generated_data(self, path, length, count):
        import pandas as pd
        df = pd.read_csv(path, sep=",")
        # return the first count columns of the df in a list
        #e.g., return [ col1_list, col2_list, ... , col_count_list]
        return [df.iloc[:, i].values.tolist() for i in range(count)]

