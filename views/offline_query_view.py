##offlien query view

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateResponseMixin
from django.db import connection
from django.db import connections
from django.db import models


time_stamps_options = [
    "2019-03-01T00:00:00",
    "2019-04-29T23:59:50",
]

class OfflineQueryView(View):
    context = {
        'title': 'Offline Queries',
        'heading': 'Welcome to the Offline Queries Page',
        'body': 'This is the body of the Offline Queries Page',
    }

    def get(self, request):
        import random
        random.seed(1)
        template = loader.get_template('offline-queries.html')

        self.context["query_frame"] = render_to_string('parts/query-box2.html', {})
        self.context["time_stamps"] = random.sample(time_stamps_options*100,100)
        return HttpResponse(template.render(self.context, request))

    def post(self, request):
        query = request.POST.get('query')
        print(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            print(row)
            self.context['rows'] = row
        return HttpResponse(self.template.render(self.context, request))