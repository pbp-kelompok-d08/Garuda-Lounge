from django.urls import path
from ProfileAktif.views import show_main

app_name = 'ProfileAktif'

urlpatterns = [
    path('', show_main, name='show_main'),
]
