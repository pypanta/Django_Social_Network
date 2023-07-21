import jwt

from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from ..models import User
from .authentication import JWTAuthentication
from .permissions import AnonPermissionOnly
from .serializers import UserRegisterSerializer, UserSerializer
from .utils import get_tokens_for_user


class Signup(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        qs = User.objects.filter(Q(username__iexact=email) |
                                 Q(email__iexact=email)).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
        else:
            raise AuthenticationFailed('Invalid username or email!')

        if user_obj.check_password(password):
            user = user_obj
        else:
            raise AuthenticationFailed('Invalid password!')

        tokens = get_tokens_for_user(user)

        response = Response()
        response.set_cookie(key='access',
                            value=tokens['access'],
                            httponly=True)
        response.set_cookie(key='refresh',
                            value=tokens['refresh'],
                            path='/api/refresh/',
                            httponly=True)
        response.data = {'refresh': tokens['refresh']}

        return response


class LogoutView(TokenBlacklistView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # refresh_token = RefreshToken(request.COOKIES.get('refresh'))
        # refresh_token.blacklist()
        # from rest_framework_simplejwt.token_blacklist import models
        # token = models.OutstandingToken.objects.get(token=refresh_token)
        # token.delete()

        response = Response()
        response.delete_cookie(key='access')
        response.delete_cookie(key='refresh', path='/api/refresh/')
        response.data = {'message': 'You are now logged out!'}

        return response


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenObtainPairSerializer

    def get(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token is None:
            raise AuthenticationFailed('Unauthorized')

        payload = jwt.decode(refresh_token,
                             settings.SECRET_KEY,
                             algorithms="HS256")
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthorized')

        tokens = get_tokens_for_user(user)

        response = Response()
        response.set_cookie(key='access',
                            value=tokens['access'],
                            httponly=True)
        # response.set_cookie(key='refresh',
        #                     value=tokens['refresh'],
        #                     path='/api/refresh/',
        #                     httponly=True)
        response.data = tokens

        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    @method_decorator(csrf_protect)
    def get(self, request):
        return Response(UserSerializer(request.user).data)
