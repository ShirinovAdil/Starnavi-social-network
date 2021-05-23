from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password

from social_network.models import *


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User serializer for registration
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = validated_data['password']
        user = User.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data['email']
        )

        if password is not None:
            user.set_password(password)
            user.save()

        return user


class UserViewSerializer(serializers.ModelSerializer):
    """
    Serializer to return user view
    """
    class Meta:
        model = User
        fields = ('username', 'name', 'email')
        read_only_fields = ('date_joined',)


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer
    """
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'likes', 'created_at', 'author']
        read_only_fields = ['likes', 'created_at']

    def get_likes(self, obj):
        return PostLike.objects.filter(post_id=obj.id).count()


class PostLikeSerializer(serializers.ModelSerializer):
    """
    A like serializer
    """
    class Meta:
        model = PostLike
        fields = ['post', 'liker', 'liked_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Users activity serializer
    """
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    last_activity = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = User
        fields = ['username', 'last_login', 'last_activity']