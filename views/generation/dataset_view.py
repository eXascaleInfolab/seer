from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.views import View

from views.generation.utils import get_dataset_info

dataset_folder = "generation/data"


class DatasetView(View):
    context = {
        'title': 'SEER - Datasets',
    }

    template = loader.get_template('generation/datasetDisplay.html')
    data_generation_sets = [("bafu", "Bafu"), ("conductivity", "Conductivity"), ("pH_accuracy", "pH_accuracy")]

    max_rows = 10000
    max_ts = 100

    def get(self, request, dataset):
        self.context['dataset'] = dataset
        self.context["data_info"] = get_dataset_info(dataset)
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request, dataset):
        original_data_set_path = f"{dataset_folder}/{dataset}/original.txt"
        import pandas as pd
        df = pd.read_csv(original_data_set_path, sep=",")
        df = df.iloc[:self.max_rows, :self.max_ts]
        # convert to list of lists

        data = [{"name": get_dataset_info(dataset)["header"][i], "data": df[col].values.tolist()} for i, col in
                enumerate(df.columns)]
        # return JsonResponse(data)
        return JsonResponse({
            'dataset': data,
            'name': dataset
        })


def remove_dataset(request, dataset):
    import shutil
    original_data_set_path = f"{dataset_folder}/{dataset}"
    target_data_set_path = f"generation/old_data/{dataset}"
    shutil.move(original_data_set_path, target_data_set_path)
    return redirect('datasets')
