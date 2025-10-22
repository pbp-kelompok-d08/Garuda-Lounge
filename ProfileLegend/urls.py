from django.urls import path
from . import views

app_name = 'ProfileLegend'

urlpatterns = [
    path('', views.legend_list, name='legend_list'),
    path('<uuid:id>/', views.legend_detail, name='legend_detail'),
]