from django.urls import path
from . import views

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
]
