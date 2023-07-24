from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'post')


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    post_images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'time_ago', 'post_images')

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
