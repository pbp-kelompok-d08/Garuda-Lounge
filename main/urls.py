from django.urls import path
from .views import show_main, login_user, logout_user, register_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register_user, name='register_user'),
]
