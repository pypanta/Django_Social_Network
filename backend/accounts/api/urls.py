from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    # path('login/', jwt_views.TokenObtainPairView.as_view(),
    #     name='token_obtain'),
    path('login/', views.LoginAPIView.as_view(),
        name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.RefreshTokenView.as_view(),
        name='token_refresh'),
    path('user/', views.UserAPIView.as_view(), name='user'),
    path('user/search/', views.UserSearchAPIView.as_view(), name='search'),
    path('user/follow/', views.FollowAPIView.as_view(), name='follow'),
    path('user/unfollow/', views.UnfollowAPIView.as_view(), name='unfollow'),
    path('user/accept/', views.AcceptFriendshipAPIView.as_view(),
        name='accept'),
    path('user/change-password/', views.ChangePasswordAPIView.as_view(),
         name='change-password'),
    path('user/<uuid:id>/edit/', views.EditProfile.as_view(),
         name='edit-profile'),
]
