from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    avatar_path = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email',
            'date_joined', 'last_login', 'posts', 'posts_count',
            'following', 'followers', 'avatar', 'avatar_path'
        )

    def get_posts(self, obj):
        return obj.posts.values()

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_following(self, obj):
        following = []
        for f in obj.following.all():
            if f.followed.avatar:
                avatar = f"http://127.0.0.1:8000/media/{f.followed.avatar}"
            else:
                avatar = ''
            following.append(
                {
                    'id': f.followed.id,
                    'first_name': f.followed.first_name,
                    'last_name': f.followed.last_name,
                    'username': f.followed.username,
                    'email': f.followed.email,
                    'avatar_path': avatar,
                    'status': f.status
                }
            )
        return following

    def get_followers(self, obj):
        followers = []
        for f in obj.followers.all():
            if f.follower.avatar:
                avatar = f"http://127.0.0.1:8000/media/{f.follower.avatar}"
            else:
                avatar = ''
            followers.append(
                {
                    'id': f.follower.id,
                    'first_name': f.follower.first_name,
                    'last_name': f.follower.last_name,
                    'username': f.follower.username,
                    'email': f.follower.email,
                    'avatar_path': avatar,
                    'status': f.status
                }
            )
        return followers

    def get_avatar_path(self, obj):
        if obj.avatar:
            return f"http://127.0.0.1:8000/media/{obj.avatar}"


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email',
            'date_joined', 'last_login', 'password', 'password_confirm'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')

        if password is None or password_confirm is None:
            raise serializers.ValidationError(
                'password and password_confirm are required fields!'
            )

        if password != password_confirm:
            raise serializers.ValidationError('Passwords must match!')

        return data

    def create(self, validated_data):
        password = validated_data.get('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = False
        instance.save()
        return instance
