from django.urls import path
from . import views

app_name = 'ProfileLegend'

urlpatterns = [
    path('', views.show_profile_legend, name='show_profile_legend'),
    path('<uuid:id>/', views.show_legend_detail, name='show_legend_detail'),
]