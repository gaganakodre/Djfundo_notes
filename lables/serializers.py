from rest_framework import serializers
from .models import Labels


class LabelSerializer(serializers.ModelSerializer):
    """
    serializer class for Notes
    """
    class Meta:
        model = Labels
        fields = ['id', 'title', 'color']
