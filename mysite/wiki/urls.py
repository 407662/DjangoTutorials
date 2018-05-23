from django.urls import path
from . import views

app_name = 'wiki'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('upload/', views.upload_view, name='upload'),

    path('', views.index_view, name='index'),
    path('<str:title>/', views.detail_view, name='detail'),
    path('<str:title>/edit/', views.EditView.as_view(), name='edit')
]
