from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'news'

urlpatterns = [
    path('', views.show_news_main, name='show_news_main'),
    path('create/', views.create_news, name='create_news'),

    # JSON/XML
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<uuid:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'),

    # CRUD
    path('<uuid:id>/', views.show_news_detail, name='show_news_detail'),
    path('<uuid:id>/edit/', views.edit_news, name='edit_news'),
    path('<uuid:id>/delete/', views.delete_news, name='delete_news'),

    # AJAX
    path('add-news-entry-ajax/', views.add_news_entry_ajax, name='add_news_entry_ajax'),
=======
app_name = "news"

urlpatterns = [
    # Halaman publik
    path("", views.show_news_main, name="show_news_main"),

    # JSON/XML (harus di atas)
    path("json/", views.show_json, name="show_json"),
    path("json/<uuid:id>/", views.show_json_by_id, name="show_json_by_id"),
    path("xml/", views.show_xml, name="show_xml"),
    path("xml/<uuid:news_id>/", views.show_xml_by_id, name="show_xml_by_id"),

    # AJAX endpoints (di atas juga)
    path("api/add/", views.add_news_entry_ajax, name="add_news_entry_ajax"),
    path("api/<uuid:id>/comments/", views.get_comments, name="get_comments"),
    path("api/<uuid:id>/comments/add/", views.add_comment, name="add_comment"),

    # Admin buatan sendiri
    path("create/", views.create_news, name="create_news"),
    path("detail/<uuid:id>/", views.show_news_detail_uuid, name="show_news_detail"),
    path("<uuid:id>/edit/", views.edit_news, name="edit_news"),
    path("<uuid:id>/delete/", views.delete_news, name="delete_news"),

    # TERAKHIR: catch-all slug untuk detail publik
    path("<slug:slug>/", views.show_news_detail_slug, name="show_news_detail_slug"),
>>>>>>> origin/feat/news
]
