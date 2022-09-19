import jwt
from django.conf import settings
from rest_framework.request import Request


class JWT:
    """
    class for generating token
    """

    @staticmethod
    def jwt_encode(payload):
        return jwt.encode(payload, settings.JWT_SECRET_KEY, "HS256")

    @staticmethod
    def jwt_decode(token):
        return jwt.decode(token, settings.JWT_SECRET_KEY, ["HS256"])


def verify_token(function):
    def wrapper(self, request):
        token = request.headers.get('token')
        if not token:
            raise Exception("Auth token required")
        decode = JWT.jwt_decode(token=token)
        user_id = decode.get('id')
        if not user_id:
            raise Exception("User not found")
        request.data.update({"user": user_id})
        return function(self, request)

    return wrapper
