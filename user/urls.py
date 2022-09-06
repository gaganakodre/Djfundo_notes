from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
]
