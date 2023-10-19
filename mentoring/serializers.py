from rest_framework import serializers

from .models import Mentor,Mentee,Session, Category

from users.models import CustomUser

class SessionSerializer(serializers.ModelSerializer):
    mentor = serializers.UUIDField(read_only=True)
    mentee = serializers.UUIDField(read_only=True)

    class Meta:
        model = Session
        fields = '__all__'
class MentorProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields='__all__'

class MenteeProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentee
        fields='__all__'  
class MentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields=['job_title' , 'company' ,'industry', 
    'experience' ,
    'skills' ,
    'linkedin' ,
    'twitter' ,
    'other_links' ,
    'mentoring_exp',
    'mentoring_type',
    'availability',
    'prefered_starttime',
    'prefered_endtime',
    'prefered_days' ,
    'education' ,
    'certification' ,
    'identity' ,
    'status' ,
    'resources' 
]
class MenteeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentee
        fields=[ 'expertise',
    'company' ,
    'title' ,
    'goals' 
] 

class UserlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','image']
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"