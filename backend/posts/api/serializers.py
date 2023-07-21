from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'post')


class PostSerializer(serializers.ModelSerializer):
    # created_by = serializers.SerializerMethodField(read_only=True)
    # user = UserSerializer(read_only=True, source='created_by')
    created_by = UserSerializer(read_only=True)
    post_images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'time_ago', 'post_images')

    # def get_created_by(self, obj):
    #     if obj.created_by.full_name:
    #         return obj.created_by.full_name
    #     elif obj.created_by.username:
    #         return obj.created_by.username
    #     else:
    #         return obj.created_by.email
