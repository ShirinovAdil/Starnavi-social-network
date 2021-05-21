from django.contrib import admin
from social_network.models import *


admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostLike)