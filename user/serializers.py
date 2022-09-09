from django.contrib.auth import authenticate
from rest_framework import serializers, status
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        extra_kwagrs = {"password": {
            "max_length": 250, "write_only": True
        }}

    def create(self, validated_data):
        """
        Create and return a new `Students` instance, given the validated data.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=250, required=True, write_only=True)

    def create(self, validate_data):
        print(validate_data)
        user = authenticate(**validate_data)

        print(user)
        if not user:
            raise serializers.ValidationError(detail='invalid credentials', code=status.HTTP_406_NOT_ACCEPTABLE)
        return user
