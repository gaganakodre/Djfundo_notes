from django.contrib.auth import authenticate
from rest_framework import serializers, status
from user.models import User
from user.token import JWT


class UserSerializer(serializers.ModelSerializer):
    """
    This Serializer class is used for user register
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        extra_kwagrs = {
            "password": {
            "max_length": 250, "write_only": True
        }}

    def create(self, validated_data):
        """
        Create and return a new `Students` instance, given the validated data.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    This Serializer class is used for user login
    """
    email = serializers.EmailField(max_length=255, required=True,write_only=True)
    password = serializers.CharField(max_length=250, required=True, write_only=True)
    token=serializers.SerializerMethodField(read_only=True)



    def create(self, validate_data):
        """
        Method to create the user login
        """
        # print(validate_data)
        user = authenticate(**validate_data)

        # print(user.id)
        if not user:
            raise serializers.ValidationError(detail='invalid credentials', code=status.HTTP_406_NOT_ACCEPTABLE)
        return user

    def get_token(self,obj):
        data={"email":obj.email, "id":obj.id}

        return JWT.jwt_encode(data)

