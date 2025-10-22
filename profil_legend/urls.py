from django.urls import path
from profil_legend import views

app_name = 'profil_legend'

urlpatterns = [
    path('', views.show_profile_list, name='show_profile_list'), 
    path('<uuid:id>/', views.show_profile_detail, name='show_profile_detail'),
]