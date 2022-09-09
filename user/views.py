from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, LoginSerializer


class UserRegisterView(APIView):
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
            email = serializer.data.get('email')
            print(email)
            password = serializer.data.get('password')
            print(password)
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request,user)
                # return Response({"status": True, "message": "login successful",
                #                  "data": "data"}, status=status.HTTP_200_OK)
                return Response({ "message": "login successful",
                                 "data": "data"}, status=status.HTTP_200_OK)
        except Exception as e:
            # return Response({"status": False, "message": "login unsuccessful",
            #                  "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({ "message": "login unsuccessful",
                             "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
