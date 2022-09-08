from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=250)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        """
        Create and return a new `Students` instance, given the validated data.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=250)
    class Meta:
        model = User
        fields = ['email', 'password']
