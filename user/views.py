from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer

import logging

logging.basicConfig(filename='Djfundo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

class UserRegisterView(APIView):
    """
    Class is to register for the user
    """

    def post(self, request):
        """
        Method is used for the user login
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("user successfully registered")
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
            return Response({"status": True, "message": e.detail,
                             }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(e)
            return Response({"status": True, "message": str(e),
                             }, status=status.HTTP_400_BAD_REQUEST)
