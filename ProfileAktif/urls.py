from django.urls import path
from ProfileAktif.views import show_main, create_player, show_player, show_xml, show_json

app_name = 'ProfileAktif'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-player/', create_player, name='create_player'),
    path('player/<uuid:id>/', show_player, name='show_player'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    # path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    # path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
]
