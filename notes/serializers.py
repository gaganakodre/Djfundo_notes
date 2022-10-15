from rest_framework import serializers

from .models import Notes


class NoteSerializer(serializers.ModelSerializer):
    """
    serializer class for Notes
    """

    class Meta:
        """
        Model Meta is basically used to change the behavior of your model fields 
        """
        model = Notes
        fields = ['id', 'title', 'description', 'user', 'labels','collaborator','is_pinned','is_archive']

        read_only_fields=['labels','collaborator','is_pinned','is_archive']


class LabelAndNotesSerializer(serializers.ModelSerializer):
    """
    serializer class for the Notes and labels
    """
    class Meta:
        model = Notes
        fields = ['labels', 'id']

class CollaboratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ['id', 'collaborator']

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'is_pinned']
        read_only_fields = ['id', 'title']

class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'is_archive']
        read_only_fields = ['id', 'title','archive']