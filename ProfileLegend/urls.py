from django.urls import path
from .views import *

app_name = 'ProfileLegend'

urlpatterns = [
    path('', show_profile_legend, name='show_profile_legend'),
    path('create/', create_legend, name='create_legend'),
    path('<uuid:id>/', show_legend_detail, name='show_legend_detail'),
    
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),

    path('add-ajax/', add_legend_ajax, name='add_legend_ajax'),
]