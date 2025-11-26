from django.urls import path
from . import views

app_name = 'main'  

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('landing/', views.show_landingpage, name='show_landingpage'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('json/', views.show_json, name='show_json'),
    path('xml/', views.show_xml, name='show_xml'),
    
    # AJAX endpoints
    path('login-ajax/', views.login_ajax, name='login_ajax'),
    path('register-ajax/', views.register_ajax, name='register_ajax'),

    path('proxy-image/', views.proxy_image, name='proxy_image'),
    path('create-match-flutter/', views.create_match_flutter, name='create_match_flutter'),
]