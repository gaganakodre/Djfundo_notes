from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, LoginSerializer




class UserRegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": True, "message": "register successfully",
                                 "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": "register Unsuccessfull",
                             "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response={"data":serializer.data,"status":200}
        except ValidationError as e:
            response={"message":e.detail,'status':e.status_code}
        except Exception as e:
            response={"message":str(e),'status':400}
        return Response(response,status=response['status'])