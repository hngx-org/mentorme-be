from rest_framework import serializers

from .models import Session, Category, Company, Industry, Mentee, Mentor,Mentee,Session, Category

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

class UserlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','image']
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class IndustrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Industry
        fields = "__all__"


class MenteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentee
        fields = "__all__"
