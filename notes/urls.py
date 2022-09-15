from django.urls import path
from . import views
from notes.views import Note

app_name = "note"
urlpatterns = [
    path('note/', Note.as_view(), name='notes_operation'),
]
