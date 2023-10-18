from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.db import connection
from django.db import connections
from django.db import models



class OfflineQueryView(View):
    context = {
        'title': 'Compression View',
    }

    def get(self, request):
        template = loader.get_template('compression.html')
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