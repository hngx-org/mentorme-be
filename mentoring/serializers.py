from rest_framework import serializers
from .models import Mentee
from users.models import CustomUser


class MenteeSerializer(serializers.ModelSerializer):
    """Serializer for the mentee model"""
    class Meta:
        model = Mentee
        fields = "__all__" #('expertise', 'company', 'title', 'goals')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""
    class Meta:
        model = CustomUser
        fields = "__all__"




