from django.conf import settings
from django.utils import timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @staticmethod
    def get_token_expiration_time():
        expire_delta = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        expiration_time = timezone.now() + expire_delta
        return expiration_time.strftime("%d-%m-%Y %H:%M:%S")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['expires'] = cls.get_token_expiration_time()

        return token
