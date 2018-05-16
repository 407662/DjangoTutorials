from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('', views.index, name='index'),
    path('<str:title>/', views.view, name='detail'),
    path('<str:title>/edit/', views.EditView.as_view(), name='edit')
]
