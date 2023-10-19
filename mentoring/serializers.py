from rest_framework import serializers
from .models import Mentor,Mentee
from users.models import CustomUser

class MentorProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields='__all__'

class MenteeProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentee
        fields='__all__'  

class UserlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','image','expertise']