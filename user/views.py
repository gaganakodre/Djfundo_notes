from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, LoginSerializer


class UserRegisterView(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": True, "message": "register successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"status": False, "message": e.detail,
                             }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": False, "message": "register Unsuccessfully",
                             "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"status": True, "message": "logged in successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"status": True, "message": e.detail,
                             }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"status": True, "message": str(e),
                             }, status=status.HTTP_400_BAD_REQUEST)
