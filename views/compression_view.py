from django.http import HttpResponse
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
                for system, compressions in system_compressions.items():
                    compression_data[type][data_set_name][system] = compressions.get(data_set_name, -1)

        print(compression_data)
        self.context['compression_data'] = json.dumps(compression_data, cls=NumpyEncoder)
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request):
        query = request.POST.get('query')
        print(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            print(row)
            self.context['rows'] = row
        return HttpResponse