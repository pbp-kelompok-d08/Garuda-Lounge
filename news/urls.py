from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.show_news, name='show_news'),
    path('create/', views.create_news, name='create_news'),
    path('<uuid:id>/', views.show_news_detail, name='show_news_detail'),
]
