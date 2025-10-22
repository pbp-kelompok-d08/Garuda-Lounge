
#Pastikan ada app_name = 'match' di file ini
#jadi seperti ini:
#app_name = 'match'
#urlpatterns = [ ...

from django.urls import path
from match import views

app_name = 'match'
urlpatterns = [
    path('', views.show_match, name='show_match'),
]