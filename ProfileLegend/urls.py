from django.urls import path
from ProfileLegend import views

app_name = 'ProfileLegend'

urlpatterns = [
    path('', views.show_profile_list, name='show_profile_list'), 
    path('<uuid:id>/', views.show_profile_detail, name='show_profile_detail'),
]