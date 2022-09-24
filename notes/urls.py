from django.urls import path
from . import views
from notes.views import Note, Collaborator,PinnedNotes,Archive,AddLabelToNote


app_name = "note"
urlpatterns = [
    path('note/', Note.as_view(), name='notes_operation'),
    path('collaborator/', Collaborator.as_view(), name='collaborator'),
    path('labels/', AddLabelToNote.as_view(), name='labels'),
    path('pinned/<int:id>', PinnedNotes.as_view(), name='pinned_notes'),
    path('archive/<int:id>', Archive.as_view(), name='Archive_notes'),

]
