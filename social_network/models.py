from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model to add extra fields
    """
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    last_activity = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    """
    Model representing a post
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.likes


class PostLike(models.Model):
    """
    A model to represent a single like
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} like by {self.liker.username}"
