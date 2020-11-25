from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from goals.serializers import GoalSerializer

from goals.models import Goal

class GoalList(ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)

    # def get_queryset(self):
    #     is_trending = self.request.query_params.get('is_trending', None)
    #     if is_trending is None:
    #         return super().get_queryset()
    #     queryset = Goal.objects.all()
    #     if is_trending.lower() == 'true':
    #         return [obj for obj in queryset if obj.trending == True]
    #     return queryset