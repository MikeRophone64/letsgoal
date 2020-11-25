from rest_framework import  serializers

from goals.models import User, Profile, Goal, Like

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'title', 'created_by', 'num_likes', 'num_supports', 'num_copies', 'trending')

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['trending'] = instance.trending()
    #     return data 

        