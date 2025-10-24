
#Pastikan ada app_name = 'match' di file ini
#jadi seperti ini:
#app_name = 'match'
#urlpatterns = [ ...

from django.urls import path
from match.views import show_match, add_match, show_match_details, delete_match, edit_match

app_name = 'match'
urlpatterns = [
    path('', show_match, name='show_match'),
    path('add-match/', add_match, name='add_match'),
    path('<str:id>', show_match_details, name='show_match_details'),
    path('<uuid:id>/delete', delete_match, name='delete_match'),
    path('<uuid:id>/edit', edit_match, name='edit_match'),
]