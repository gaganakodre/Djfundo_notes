import json

from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from user.models import User


# Create your views here.

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        details = User.objects.create(**data)
        print(details)
        return JsonResponse({"message": "sucessfully contact added"})

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # email = requdata.get("email")
        # print(email)
        # password = data.get("password")
        # print(password)
        user = authenticate(username=data.get("username"), password=data.get("password"))
        print(user)
        if user is not None:
            return JsonResponse({"login sucessfull"})
        return JsonResponse({"message":"check your credentials"})
        # details = Registration.objects.get(email=email)
        # print(details.password)
        # print(password)


        # if details.password == password:
        #     return JsonResponse({"login sucessfull"})
