from rest_framework import generics, status
from rest_framework.response import Response

from accounts.api.authentication import JWTAuthentication

from ..models import Post
from .serializers import PostSerializer


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # serializer.save(created_by=self.request.user,
        #                 images=self.request.data.get('images'))
        serializer.save(
            created_by=self.request.user,
            images=[i for i in self.request.data.getlist('images')]
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
