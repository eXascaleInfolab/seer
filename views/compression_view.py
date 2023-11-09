from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View

from django.db import connection
from utils.compression_loader import load_compression_data_sets, load_systems_compression
from utils.numpy_loader import NumpyEncoder
import json

class CompressionView(View):
    context = {
        'title': 'Compression View',
    }
    template = loader.get_template('compression.html')

    def get(self, request):
        print("GETTING COMPRESSION VIEW")
        data_sets = load_compression_data_sets()
        system_compressions = load_systems_compression()

        # generate compression data
        compression_data = {}
        for type, data_sets in data_sets.items():
            compression_data[type] = {}
            for data_set_name, data in data_sets.items():
                compression_data[type][data_set_name] = {}
                compression_data[type][data_set_name]['data'] = data
                compression_data[type][data_set_name]['compression'] = {}
                for system, compressions in system_compressions.items():
                    compression_data[type][data_set_name]['compression'][system] = compressions.get(f"{type}_{data_set_name}", (-1,-1))[0]

        #print(compression_data)
        self.context['compression_data'] = json.dumps(compression_data, cls=NumpyEncoder)
        return HttpResponse(self.template.render(self.context, request))

    # def post(self, request):
    #     print("POSTING COMPRESSION VIEW")
    #     data_set = request.POST.get('data_set')
    #     data_type = request.POST.get('data_type')
    #
    #     # load_dataset
    #     data_sets = load_compression_data_sets()
    #
    #     return JsonResponse(data)