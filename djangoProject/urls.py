"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views.index_view import IndexView
from views.live_queries_view import LiveQueryView
from views.offline_query_view import OfflineQueryView, OnlineQueryView
from views.compression_view import CompressionView
from views.generation_view import GenerationView
from views.datasets_view import DatasetsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view() , name='index'),
    path('queries', OfflineQueryView.as_view() , name='offline-queries'),
    path('queries-online', OnlineQueryView.as_view(), name='online-queries'),
    path('queries-live' , LiveQueryView.as_view(),name= 'live-queries'),

    path('compression', CompressionView.as_view(), name='compression'),
    path('datasets', DatasetsView.as_view(), name='datasets'),
    path('generation/<str:dataset>', GenerationView.as_view(), name='generation'),
]
