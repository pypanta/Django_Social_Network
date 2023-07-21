from rest_framework import generics

from accounts.api.authentication import JWTAuthentication

from ..models import Post
from .serializers import PostSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer
