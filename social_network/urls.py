from django.urls import path
from rest_framework.routers import SimpleRouter

from social_network.views import *

router = SimpleRouter()
router.register('posts', PostViewSet)

urlpatterns = [

]

urlpatterns += router.urls
