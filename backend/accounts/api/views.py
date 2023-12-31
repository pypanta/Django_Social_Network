import jwt

from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import generics, status, filters
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


class UserSearchAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'username',
                     'email', 'posts__body']
    ordering_fields = ['first_name', 'last_name', 'username', 'email']


class FollowAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.data.get('id')
        to_follow = User.objects.filter(id=user_id).first()
        if to_follow:
            user = request.user
            friendship, created = user.follow(to_follow)
            if created:
                return Response({'message': f'Follow: {to_follow}'},
                                status=status.HTTP_200_OK)
            if friendship and not created:
                return Response(
                    {'message': f'You already follow {to_follow}'})
        return Response({'message': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)


class UnfollowAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.data.get('id')
        to_unfollow = User.objects.filter(id=user_id).first()
        if to_unfollow:
            user = request.user
            friendship = user.unfollow(to_unfollow)
            if friendship:
                return Response({'message': f'Unfollow: {to_unfollow}'},
                                status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': f'{to_unfollow} is not in followed users'})
        return Response({'message': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)


class AcceptFriendshipAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        follower_id = request.data.get('id')
        status = request.data.get('status')
        friendship_request = user.followers.filter(
            follower__id=follower_id)

        if friendship_request.exists():
            friend = friendship_request.first()
            if friend.status == 'PE' and status == 'accept':
                friend.status = 'AC'
                friend.save()
                return Response({'message': 'Friendship request is accepted'})
            elif friend.status == 'PE' and status == 'reject':
                friend.delete()
                return Response({'message': 'Friendship request is rejected'})
            else:
                return Response(
                    {'message': 'Friendship request is on pending'})
        return Response({'message': 'Friendship not found'})
