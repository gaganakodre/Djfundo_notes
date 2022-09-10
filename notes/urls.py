from django.urls import path
from . import views

app_name = "note"
urlpatterns = [
    path('note/', views.Note.as_view(), name='notes_operation'),
]
