from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username',
            'email', 'date_joined', 'last_login', 'posts'
        )

    def get_posts(self, obj):
        return obj.posts.values()


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
        instance.is_active = True
        instance.save()
        return instance
