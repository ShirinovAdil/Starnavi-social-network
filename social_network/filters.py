from django_filters import rest_framework as filters
from social_network.models import *


class LikeAnalyticsFilter(filters.FilterSet):
    year = filters.DateFromToRangeFilter(method='filter_likes_analytics')

    class Meta:
        model = Post
        fields = ['post_likes']

    def filter_likes_analytics(self, queryset, name, value):
        print(queryset)
        print(name)
        print(value.year_after)
