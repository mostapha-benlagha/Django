"""
Custom JWT authentication for MongoDB users.
"""
from bson import ObjectId
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from api.models import User


class MongoDBJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that works with MongoDB users.
    Overrides the default authentication to use MongoDB User model instead of Django's User.
    """

    def get_user(self, validated_token):
        """
        Returns a MongoDB user instance from the validated token payload.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as e:
            raise InvalidToken(
                "Token contained no recognizable user identification"
            ) from e

        try:
            # Convert string ID to ObjectId for MongoDB query
            # mongoengine can handle both, but being explicit is safer
            try:
                user_id_obj = ObjectId(user_id)
                user = User.objects.get(id=user_id_obj)
            except (ValueError, TypeError):
                # If ObjectId conversion fails, try with string directly
                user = User.objects.get(id=user_id)
        except Exception:
            raise AuthenticationFailed("User not found", code="user_not_found")

        # The User model now has is_authenticated, is_active, and is_anonymous as properties
        # No need to set them manually

        return user

