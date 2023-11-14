##offlien query view

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
from utils.CONSTANTS import INFLUX, QUESTDB, TIMESCALEDB, MONETDB, EXTREMEDB, CLICKHOUSE, DRUID



# Random settings
#d1 2019-03-01T00:00:00 - 2019-04-29T23:59:40 , stations st0 - st9     , sensors s0 - s99
#d2 2019-02-01T00:00:10 - 2019-02-10T23:59:50 , stations st0 - st1999 ,  sensors s0 - s99



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
        template = loader.get_template('offline-queries/offline-queries.html')

        self.context["query_frame"] = render_to_string('offline-queries/query-box2.html', {})
        self.context["time_stamps"] = random.sample(time_stamps_options*100,100)
        return HttpResponse(template.render(self.context, request))

    def post(self, request):
        query = request.POST.get('query')

        #test data for now
        data = { INFLUX : 1 , QUESTDB  : 3 , TIMESCALEDB : 2 , MONETDB : 4 , EXTREMEDB : 5 , CLICKHOUSE : 6 , DRUID : 7}
        print(data)

        self.context["data"] = data
        # return json respone
        return JsonResponse(data)

