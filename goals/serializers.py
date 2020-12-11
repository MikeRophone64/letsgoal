from rest_framework import  serializers

from goals.models import User, Profile, Goal, Like

class GoalSerializer(serializers.ModelSerializer):
    is_trending = serializers.BooleanField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)

    class Meta:
        model = Goal
        fields = (
            'id', 'title', 'description', 'created_by', 'category', 'term', 
            'deadline', 'amount', 'num_likes', 'num_supports', 'num_copies', 'is_trending',
            )


        