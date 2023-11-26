from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Comment, Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'post')


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'time_ago')

    def create(self, validated_data):
        post = validated_data.pop('post')
        comment = Comment.objects.create(**validated_data)
        post.comments.add(comment)
        return comment


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    post_images = PostImageSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'likes_count',
                  'liked_by', 'time_ago', 'post_images', 'comments')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by(self, obj):
        return obj.likes.values()

    def create(self, validated_data):
        data = {
            'body': validated_data.get('body'),
            'created_by': validated_data.get('created_by')
        }

        post = Post.objects.create(**data)

        if 'images' in validated_data:
            # PostImage.objects.create(image=validated_data['images'],
            #                          post=post)
            PostImage.objects.bulk_create(
                [
                    PostImage(image=i, post=post)
                    for i in validated_data['images']
                ]
            )
        return post
