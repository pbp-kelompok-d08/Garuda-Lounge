from django.urls import path
from . import views

app_name = 'main'  

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path('landing/', views.show_landingpage, name='show_landingpage'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('json/', views.show_json, name='show_json'),
    path('xml/', views.show_xml, name='show_xml'),
]
