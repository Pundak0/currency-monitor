from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('', views.index, name='index'),
    path('chart/', views.chart_view, name='chart'),
    path('profile/', views.profile, name='profile'),
]