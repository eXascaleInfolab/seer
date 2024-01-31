##django index view with index tempalte


from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateResponseMixin


class IndexView(View):
    def get(self, request):
        template = loader.get_template('index.html')
        context = {
            'title': 'SEER',
            'heading': 'Welcome to the Index Page',
            'body': 'This is the body of the Index Page',
        }
        return HttpResponse(template.render(context, request))

class AboutView(View):
    def get(self, request):
        template = loader.get_template('about.html')
        context = {
            'title': 'About SEER',
            'heading': 'Welcome to the About Page',
            'body': 'This is the body of the Index Page',
        }
        return HttpResponse(template.render(context, request))

