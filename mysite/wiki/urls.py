from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.index, name='index'),
    path(r'^(?P<pk>\d+)$', views.index, name='page')
]
