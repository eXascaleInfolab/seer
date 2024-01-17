from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

from views.generation.utils import generation_datasets_info

dataset_folder = "generation/data"
class DatasetView(View):
    context = {
        'title': 'TSM - Datasets',
    }

    template = loader.get_template('generation/datasetDisplay.html')
    data_generation_sets = [("bafu", "Bafu"), ("conductivity", "Conductivity"), ("pH_accuracy", "pH_accuracy")]

    max_rows = 10000
    max_ts = 100

    def get(self, request, dataset):
        self.context['dataset'] = dataset
        self.context["data_info"] = generation_datasets_info[dataset]
        return HttpResponse(self.template.render(self.context, request))

    def post(self,request, dataset):
        original_data_set_path = f"{dataset_folder}/{dataset}/original.txt"
        import pandas as pd
        df = pd.read_csv(original_data_set_path, sep=",")
        df = df.iloc[:self.max_rows, :self.max_ts]
        # convert to list of lists

        data = [ { "name" :  dataset+str(i+1) ,  "data" :  df[col].values.tolist()  } for i, col in enumerate(df.columns)]
        # return JsonResponse(data)
        return JsonResponse({
            'dataset': data,
            'name':    dataset
        })
