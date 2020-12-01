from django.http import HttpResponseRedirect
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from goals.serializers import GoalSerializer
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Goal

class GoalPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class GoalList(ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('title', 'description')
    pagination_class = GoalPagination

    # def get_queryset(self):
    #     is_trending = self.request.query_params.get('is_trending', None)
    #     if is_trending is None:
    #         return super().get_queryset()
    #     queryset = Goal.objects.all()
    #     if is_trending.lower() == 'true':
    #         return [obj for obj in queryset if obj.trending == True]
    #     return queryset

class GoalCreate(CreateAPIView):
    serializer_class = GoalSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class GoalRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    lookup_field = 'id'
    serializer_class = GoalSerializer

    def delete(self, request, *args, **kwargs):
        goal_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('goal_data_{}'.format(goal_id))
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            goal = response.data
            cache.set('goal_data_{}'.format(goal['id']), {
                "title": goal['title'],
                "description": goal['description']
            })
        return response