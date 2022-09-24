from django.urls import path
from . import views
from lables.views import Label

app_name = "note"
urlpatterns = [
    path('label/', Label.as_view(), name='label_operation'),
]