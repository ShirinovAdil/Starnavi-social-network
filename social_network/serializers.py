from rest_framework import serializers
from social_network.models import *


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'likes', 'created_at', 'author']
        read_only_fields = ['likes', 'created_at']

    def get_likes(self, obj):
        return PostLike.objects.filter(post_id=obj.id).count()