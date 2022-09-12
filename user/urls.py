from django.urls import path
from user.views import UserRegisterView, UserLoginView

app_name = "user"
urlpatterns = [

    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),

]
