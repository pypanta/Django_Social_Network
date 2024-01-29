import jwt

from django.conf import settings
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    NumericPasswordValidator,
    validate_password
)
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import filters, generics, status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
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
        user = serializer.save()

        # Send account activation e-mail
        url = f"http://127.0.0.1:8000/accounts/activate/{user.id}"
        send_mail(
            "Please verify your e-mail address",
            f"Click on: {url} URL address to activate your account.",
            "noreply@example.com",
            [user.email],
            fail_silently=False,
        )

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

        if not user_obj.is_active:
            raise AuthenticationFailed(
                'Your account is not activated! Please, check your e-mail.')

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


class EditProfile(generics.UpdateAPIView):
    """View for handling user profile editing."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'

    def get_object(self):
        """Get the user object for the profile being edited."""
        user_obj = self.request.user
        profile_id = self.kwargs[self.lookup_field]

        if user_obj.id != profile_id:
            raise PermissionDenied(
                "You do not have permission to edit this profile.")
        return user_obj

    def update(self, request, *args, **kwargs):
        """Handles PUT requests for updating a user's profile."""
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ChangePasswordAPIView(APIView):
    """API view for changing user password."""
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        Handle the password change process.

        Parameters:
            - request: HTTP request object containing user and password data.
        """
        user = request.user
        data = request.data

        # Checks the current user password
        if not user.check_password(data.get('old_password')):
            return Response({'message': 'Your old password is not valid!'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Check if the new password and its confirmation match
        if data.get('new_password') != data.get('new_password_confirm'):
            return Response({
                'message': f"New password and new password confirm must "
                           f"be the same!"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Validate the new password using Django password validators
        try:
            validate_password(password=data.get('new_password'),
                              user=user,
                              password_validators=[
                                  NumericPasswordValidator(),
                                  MinimumLengthValidator(min_length=4)
                              ]
            )
        except ValidationError as e:
            return Response({'message': f"{' '.join(m for m in e.messages)}"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Set the new password for the user and save the changes
        user.set_password(data.get('new_password'))
        user.save()

        return Response({'message': 'Your password is successfully changed!'},
                        status=status.HTTP_200_OK)
