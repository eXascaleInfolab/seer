from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

from django.db import connection
from utils.compression_loader import load_compression_data_sets, load_systems_compression
from utils.numpy_loader import NumpyEncoder, convert_np_values
import json

data_sets = load_compression_data_sets()
system_compressions = load_systems_compression()

compression_data = {}
for type_, data_sets in data_sets.items():
    compression_data[type_] = {}
    for data_set_name, data in data_sets.items():
        compression_data[type_][data_set_name] = {}
        compression_data[type_][data_set_name]['data'] = data
        compression_data[type_][data_set_name]['compression'] = {}
        for system, compressions in system_compressions.items():
            compression_data[type_][data_set_name]['compression'][system] = \
            compressions.get(f"{type_}_{data_set_name}", (-1, -1))[0]


class CompressionView(View):
    context = {
        'title': 'Compression View',
    }
    template = loader.get_template('compression/compression.html')

    def get(self, request):
        print("GETTING COMPRESSION VIEW")
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request):
        print("POSTING COMPRESSION VIEW")
        dataType = request.POST.get("dataType")
        dataset = request.POST.get('dataset')

        # print(compression_data[dataTyp   e])
        data  =compression_data[dataType]
        result = {"data": data}
        result = convert_np_values(result)

        return JsonResponse(result)
