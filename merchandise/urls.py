from django.urls import path
from merchandise import views

app_name = 'merchandise'
urlpatterns = [
    path('', views.show_merch, name='show_merch'),
    ]