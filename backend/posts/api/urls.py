from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='posts'),
    path('<uuid:user_id>/', views.PostListAPIView.as_view(),
        name='user_posts'),
]
