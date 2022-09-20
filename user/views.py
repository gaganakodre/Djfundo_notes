import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from user.token import JWT
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .task import email_sender
from .utils import Util

logging.basicConfig(filename='Djfundo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


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
            logger.info("user successfully registered")
            Util.user_verify_user(id=serializer.data.get("id"), email=serializer.data.get("email"))
            return Response({"status": True, "message": "register successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)

        except ValidationError as e:
            logger.error(e)
            return Response({"status": False, "message": e.detail,
                             }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(e)
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
            logger.info("user successfully logged in")
            return Response({"status": True, "message": "logged in successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(e)
            return Response({"status": False, "message": e.detail,
                             }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(e)
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
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
