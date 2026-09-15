from rest_framework import serializers
from .models import *

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

class MembersSerializer(serializers.ModelSerializer):
    community = serializers.CharField(read_only = True)
    user = serializers.CharField(read_only = True)
    class Meta:
        model = Members
        fields = '__all__'
    
    

