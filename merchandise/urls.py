from django.urls import path
from merchandise import views

app_name = 'merchandise'
urlpatterns = [
    path('', views.show_merch, name='show_merch'),
    path('create/', views.create_merch, name='create_merch'),

    # JSON/XML
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<uuid:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'),

    # CRUD
    path('<uuid:id>/', views.show_merch_detail, name='show_merch_detail'),
    path('<uuid:id>/edit/', views.edit_merch, name='edit_merch'),
    path('<uuid:id>/delete/', views.delete_merch, name='delete_merch'),

    # AJAX
    path('add-merch-entry-ajax/', views.add_merch_entry_ajax, name='add_merch_entry_ajax'),
    ]