from django.urls import path, include
from . import views

app_name = "news"

urlpatterns = [
    # Halaman utama
    path("", views.show_news_main, name="show_news_main"),

    # JSON/XML
    path("json/", views.show_json, name="show_json"),
    path("json/<uuid:id>/", views.show_json_by_id, name="show_json_by_id"),
    path("xml/", views.show_xml, name="show_xml"),
    path("xml/<uuid:news_id>/", views.show_xml_by_id, name="show_xml_by_id"),

    # AJAX / API
    path("api/add/", views.add_news_entry_ajax, name="add_news_entry_ajax"),
    path("api/<uuid:id>/comments/", views.get_comments, name="get_comments"),
    path("api/<uuid:id>/comments/add/", views.add_comment, name="add_comment"),

    # Flutter endpoint (HARUS sebelum slug catch-all)
    path("create-flutter/", views.create_news_flutter, name="create_news_flutter"),

    # Proxy image
    path("proxy-image/", views.proxy_image, name="proxy_image"),

    # Admin pages
    path("create/", views.create_news, name="create_news"),
    path("detail/<uuid:id>/", views.show_news_detail_uuid, name="show_news_detail"),
    path("<uuid:id>/edit/", views.edit_news, name="edit_news"),
    path("<uuid:id>/delete/", views.delete_news, name="delete_news"),

    # Auth urls (kalau beneran butuh di sini)
    path("auth/", include("authentication.urls")),

    # TERAKHIR: catch-all slug
    path("<slug:slug>/", views.show_news_detail_slug, name="show_news_detail_slug"),
]
