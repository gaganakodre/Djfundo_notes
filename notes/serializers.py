from rest_framework import serializers
from .models import Notes


class NoteSerializer(serializers.ModelSerializer):
    """
    serializer class for Notes
    """
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user']
