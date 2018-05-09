from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:title>/', views.view, name='detail'),
    path('<str:title>/edit/', views.EditView.as_view(), name='edit')
]
