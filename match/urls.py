
#Pastikan ada app_name = 'match' di file ini
#jadi seperti ini:
#app_name = 'match'
#urlpatterns = [ ...

from django.urls import path
from match.views import show_match, show_match_details, delete_match
from match.views import show_match_json, add_match_ajax, get_edit_form_html, edit_match_ajax
from match.views import create_match_flutter, edit_match_flutter, delete_match_flutter

app_name = 'match'
urlpatterns = [
    path('', show_match, name='show_match'),
    # path('add-match/', add_match, name='add_match'),
    path('<str:id>', show_match_details, name='show_match_details'),
    path('<uuid:id>/delete', delete_match, name='delete_match'),
    # path('<uuid:id>/edit', edit_match, name='edit_match'),
    path('json/', show_match_json, name='show_match_json'),
    # path('json/<str:match_id>/', show_json_by_id, name='show_json_by_id'),
    path('add-match-ajax/', add_match_ajax, name='add_match_ajax'),
    path('<uuid:id>/get-form-html/', get_edit_form_html, name='get_edit_form_html'),
    path('<uuid:id>/edit-ajax/', edit_match_ajax, name='edit_match_ajax'),
    path('create-match-flutter/', create_match_flutter, name='create_match_flutter'),
    path('edit-match-flutter/<uuid:id>/', edit_match_flutter, name='edit_match_flutter'),
    path('delete-match-flutter/<uuid:id>/', delete_match_flutter, name='delete_match_flutter'),
]