from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

from django.db import connection
from utils.compression_loader import load_compression_data_sets, load_systems_compression
from utils.numpy_loader import NumpyEncoder
import json

data_sets = {
    "d1": {"name": "D-LONG",
           "link": "http://www.bafu.admin.ch/",
           "source": "Federal Office for the Environment FOEN",
           "sensors": 100,
           "stations": 10,
           "range": "60  days",
           "data_points": "518M", },
    "d2": {"name": "D-MULTI",
           "link": "http://www.bafu.admin.ch/",
           "source": "Federal Office for the Environment FOEN",
           "sensors": 100,
           "stations": 2000,
           "range": "10  days",
           "data_points": "17.2B", }
}

with open('generation_data/datasets.json', 'r') as file:
    generation_datasets = json.load(file)

class DatasetsView(View):
    context = {
        'title': 'TSM - Datasets',
    }
    template = loader.get_template('datasets.html')
    data_generation_sets = [("bafu", "Bafu"), ("conductivity", "Conductivity"), ("pH_accuracy", "pH_accuracy")]

    def get(self, request):
        self.context['data_sets'] = data_sets
        self.context['original_data_sets'] = generation_datasets

        return HttpResponse(self.template.render(self.context, request))
