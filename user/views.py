import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# from user.models import User


# Create your views here.

@csrf_exempt
def user_register(request):
    """
    Function used for the user registration
    """
    response = {"message": "successfully contact added", "status": 201}

    try:
        if request.method == "POST":
            data = json.loads(request.body)
            details = User.objects.create_user(**data)
            print(details)
        else:
            response.update(message="method not allowed", status=405)

    except Exception as e:
        response.update(message=str(e), status=400)
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
def user_login(request):
    """
    Function used for the user login
    """
    response={"message": "logged in successfully","status":200}

    try:
        if request.method == "POST":
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                response.update(message="invalid credentials",status=400)
        else:
            response.update(message="method not allowed",status=405)

    except Exception as e:
        response.update(message=str(e), status=400)
    return JsonResponse(response, status=response.get("status"))

