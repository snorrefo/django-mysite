from django.urls import path

from . import views

app_name = 'chartjs'
urlpatterns = [
    # ex: /chartjs/
    path('', views.index, name='index'),
    path('json/', views.json, name='json'),
]
