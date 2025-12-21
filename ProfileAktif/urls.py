from django.urls import path
from ProfileAktif.views import (
    show_main,
    create_player,
    show_player,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
    add_player_ajax,
    edit_player,
    delete_player,
    proxy_image,
    create_player_flutter,
    delete_player_flutter,
    edit_player_flutter,
)

app_name = 'ProfileAktif'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-player/', create_player, name='create_player'),
    path('player/<uuid:id>/', show_player, name='show_player'),
    path('player/<uuid:id>/edit/', edit_player, name='edit_player'),
    path('player/<uuid:id>/delete/', delete_player, name='delete_player'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:player_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:player_id>/', show_json_by_id, name='show_json_by_id'),
    path('add-player-ajax/', add_player_ajax, name='add_player_ajax'),
    path("proxy-image/", proxy_image, name="proxy_image"),
    path("create-flutter/", create_player_flutter, name="create_player_flutter"),
    path("delete-flutter/<uuid:id>/", delete_player_flutter, name="delete_player_flutter"),
    path("edit-flutter/<uuid:id>/", edit_player_flutter, name="edit_player_flutter"),

]
