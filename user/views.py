from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from user.token import JWT
from .models import User
from django.conf import settings
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema

from send import task
from note_log import get_logger

lg=get_logger(name="rabbitmq",file_name="fundoo_note.log")


class UserRegisterView(GenericAPIView):
    """
    Class is to register for the user
    """
    serializer_class = UserSerializer

    def post(self, request):
        """
        Method is used for the user login
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Util.user_verify_user(id=serializer.data.get("id"),email=serializer.data.get("email"))
            token = JWT().jwt_encode({"user_id": serializer.data.get(
                "id"), "username": serializer.data.get("username")})
            message = settings.BASE_URL + "/user/verify/"+token
            print(message)
            recipent = serializer.data.get('email')
            data = {'email': serializer.data.get('email'), 'message':message}
            task(data)
                               

            return Response({"status": True, "message": "register successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)

        except ValidationError as e:
            lg.error(e)
            return Response({"status": False, "message": e.detail,
                             }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            lg.error(e)
            return Response({"status": False, "message": "register Unsuccessfully",
                             "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    This class is used for the User login
    """

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        """
        Method is used for the user login
        """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # task(serializer.data,"login")
            lg.info("user successfully logged in")
            return Response({"status": True, "message": "logged in successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            lg.error(e)
            return Response({"status": False, "message": e.detail,
                             }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            lg.error(e)
            return Response({"status": False, "message": str(e),
                             }, status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    """
    Validating the token if the user is valid or not
    """

    def get(self, request, token):
        try:
            decode_token = JWT.jwt_decode(token=token)
            user = User.objects.get(email=decode_token.get('email'))
            print(decode_token.get('email'))
            user.is_verified = True
            user.save()
            return Response({"message": "Validation Successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            lg.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
