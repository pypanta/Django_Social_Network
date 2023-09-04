from django.db.models import Q

from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.authentication import JWTAuthentication
from accounts.api.serializers import UserSerializer
from accounts.models import User

from ..models import Like, Post
from .serializers import PostSerializer


class PostListAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    def get_object(self):
        if 'user_id' in self.request.data:
            user_id = self.request.data.get('user_id')
        elif 'user_id' in self.kwargs:
            user_id = self.kwargs.get('user_id')
        else:
            user_id = None

        obj = None
        if user_id is not None:
            obj = User.objects.get(id=user_id)
            self.check_object_permissions(self.request, obj)
            return obj

        return obj

    def get_queryset(self):
        obj = self.get_object()
        if obj is not None:
            return Post.objects.filter(created_by=obj)

        # Filter user and his friends posts only
        queryset = Post.objects.filter(
            Q(created_by=self.request.user) |
            Q(created_by_id__in=self.request.user.friendships.all())
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = self.get_object()
        posts_serializer = self.get_serializer(queryset, many=True)

        if obj is not None:
            user_serializer = UserSerializer(obj)
            return Response({
                'user': user_serializer.data,
                'posts': posts_serializer.data
            })

        return Response(posts_serializer.data)

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


class PostSearchAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['body', 'created_by', 'created_at']
    search_fields = ['body', 'created_by__username']


class LikeAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, post_id=None):
        post = Post.objects.get(id=post_id)
        if post.created_by.id == request.user.id:
            return Response({"message": "You can't like your own post"})
        liked = post.likes.filter(created_by=request.user).first()
        if liked is None:
            like = Like.objects.create(created_by=request.user)
            post.likes.add(like)
            return Response({'message': 'Liked'})
        liked.delete()
        return Response({'message': 'Unliked'})
