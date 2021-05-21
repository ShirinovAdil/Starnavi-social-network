from django.shortcuts import get_object_or_404


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from social_network.serializers import *
from social_network.models import *


class PostViewSet(viewsets.ModelViewSet):
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
        #post = get_object_or_404(PostLike, post_id=pk, liker_id=request.user.id)
        # # if post:
        # #     return Response({'status': 'This post has been liked by you'})
        # # else:
        # #
