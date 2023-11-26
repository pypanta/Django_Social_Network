from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='posts'),
    path('search/', views.PostSearchAPIView.as_view(), name='search'),
    path('post/<uuid:id>/', views.PostDetailAPIView.as_view(),
        name='post_detail'),
    path('<uuid:post_id>/like/', views.LikeAPIView.as_view(), name='like'),
    path('<uuid:post_id>/comment/', views.CommentAPIView.as_view(), name='comment'),
    path('<uuid:user_id>/', views.PostListAPIView.as_view(),
        name='user_posts'),
]
