from django.urls import path
from merchandise import views

app_name = 'merchandise'
urlpatterns = [
    path('', views.show_merch, name='show_merch'),
    path('create-merch/', views.create_merch, name='create_merch'),
    path('<uuid:id>/', views.show_merch_detail, name='show_merch_detail'),
    ]