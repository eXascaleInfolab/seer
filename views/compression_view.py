from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.db import connection
from django.db import connection
from utils.compression_loader import load_compression_data_sets
from utils.numpy_loader import NumpyEncoder
import json

class CompressionView(View):
    context = {
        'title': 'Compression View',
    }

    def get(self, request):
        print("GETTING COMPRESSION VIEW")
        template = loader.get_template('compression.html')
        data_sets = load_compression_data_sets()
        self.context['data_sets'] = json.dumps(data_sets, cls=NumpyEncoder)
        return HttpResponse(template.render(self.context, request))

    def post(self, request):
        query = request.POST.get('query')
        print(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            print(row)
            self.context['rows'] = row
        return HttpResponse