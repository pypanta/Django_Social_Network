from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='posts'),
    path('search/', views.PostSearchAPIView.as_view(), name='search'),
    path('<uuid:user_id>/', views.PostListAPIView.as_view(),
        name='user_posts'),
]
