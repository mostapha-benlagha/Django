from api.models import User
from api.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


def register(data):
    """
    Register a new user and return JWT tokens.
    """
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate JWT tokens for the newly registered user
        refresh = RefreshToken()
        # Note: Since we're using MongoDB with mongoengine, we need to use the user's ID
        # as a string for the token payload
        refresh["user_id"] = str(user.id)

        return {
            "success": True,
            "data": {
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
        }
    return {"success": False, "errors": serializer.errors}


def login(data):
    """
    Authenticate a user and return JWT tokens.
    """
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {
            "success": False,
            "errors": {"detail": "Username and password are required"},
        }

    try:
        user = User.objects.get(username=username)
    except Exception:  # mongoengine doesn't have DoesNotExist, use generic exception
        return {
            "success": False,
            "errors": {"detail": "Invalid credentials"},
        }

    # Check password
    if not check_password(password, user.password):
        return {
            "success": False,
            "errors": {"detail": "Invalid credentials"},
        }

    # Generate JWT tokens
    refresh = RefreshToken()
    refresh["user_id"] = str(user.id)

    return {
        "success": True,
        "data": {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        },
    }
