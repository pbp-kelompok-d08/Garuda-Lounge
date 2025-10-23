
#Pastikan ada app_name = 'match' di file ini
#jadi seperti ini:
#app_name = 'match'
#urlpatterns = [ ...

from django.urls import path
from match.views import show_match, add_match

app_name = 'match'
urlpatterns = [
    path('', show_match, name='show_match'),
    path('add-match/', add_match, name='add_match'),
]