from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from social_network.views import *

router = SimpleRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('users/register', RegisterApiView.as_view()),
    path('users/login', LoginApiView.as_view()),
    path('users/', UsersListApiView.as_view()),
    path('users/analytics', UserAnalyticsApiView.as_view()),

    re_path(r'posts/analytics/date_from=(?P<date_from>\d{4}-\d{2}-\d{2})&date_to=(?P<date_to>\d{4}-\d{2}-\d{2})/$', PostLikesAnalyticsApiView.as_view(), name='post_likes_analytics'),

]

urlpatterns += router.urls
