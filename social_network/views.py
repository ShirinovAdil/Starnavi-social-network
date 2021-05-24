from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from social_network.serializers import *
from social_network.models import *

from .permissions import IsAuthorOrReadOnly


class RegisterApiView(APIView):
    """
    Accepts name, username, email, password, password2
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class LoginApiView(APIView):
    """
    Login via username and password
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        user = User.objects.filter(email=email, username=username).first()
        if user is None:
            raise AuthenticationFailed("Wrong credentials")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        return Response({
            'message': 'success'
        })


class PostViewSet(viewsets.ModelViewSet):
    """
     Post related endpoints.
     like_post to like the post
     unlike_post to unlike the post
    """
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly,]

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_name='like',
            permission_classes=[IsAuthenticated])
    def like_post(self, request, pk=None):
        try:
            post = PostLike.objects.get(post_id=pk, liker_id=request.user.id)
            return Response({'status': 'This post has been liked by you'})
        except PostLike.DoesNotExist:
            PostLike.objects.create(post_id=pk, liker_id=request.user.id)
            return Response({'status': 'Success'})

    @action(detail=True, methods=['post'], url_name='unlike',
            permission_classes=[IsAuthenticated])
    def unlike_post(self, request, pk=None):
        try:
            post = PostLike.objects.get(post_id=pk, liker_id=request.user.id)
            post.delete()
            return Response({'status': "You've unliked the post"})
        except PostLike.DoesNotExist:
            return Response({'status': "You can't unlike the post you have not liked"})


class PostLikesAnalyticsApiView(APIView):
    """
    An api view that return likes analytics about posts
    """

    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        likes_analytics = PostLike.objects.filter(liked_at__range=[kwargs['date_from'], kwargs['date_to']])
        if len(likes_analytics) > 0:
            return Response({'Likes': len(likes_analytics)})
        else:
            return Response({'message': "No likes"})


class UserAnalyticsApiView(APIView):
    """
    An api view that return users analytics
    """
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserActivitySerializer(users, many=True)
        return Response(serializer.data)


class UsersListApiView(APIView):
    """
    An api view that returns users list
    """
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserViewSerializer(users, many=True)
        return Response(serializer.data)
