from rest_framework import serializers
import re
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name','full_name','email', 'image', 'gender', 'country')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


    def validate_bio(self, value):
        sql_injection_pattern = r'[;\'"]'
        if re.search(sql_injection_pattern, value):
            raise serializers.ValidationError("Bio contains potentially malicious content.")

        if len(value) > 250:
            raise serializers.ValidationError("Bio cannot exceed 250 characters.")

        return value
    
class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'
    
    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative.")
        return value

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ('id', 'name')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Session
        field = '__all__'

class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        models = Identity
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        models = Certification
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        models = Resource
        fields = '__all__'


class MentorProfileSerializer(serializers.Serializer):
    custom_user = CustomUserSerializer()
    education = serializers.PrimaryKeyRelatedField(queryset=Education.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all())
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all())
    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all())
    identity = serializers.PrimaryKeyRelatedField(queryset=Identity.objects.all())
    certification = serializers.PrimaryKeyRelatedField(queryset=Certification.objects.all())
    resource = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())
    mentor = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())

    class Meta:
        models = Mentor
        fields = "__all__"

from rest_framework import serializers
from .models import Mentor

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = (
            'id', 'user', 'job_title', 'company', 'industry', 'experience',
            'skills', 'linkedin', 'twitter', 'other_links', 'mentoring_exp',
            'mentoring_type', 'availability', 'prefered_starttime', 'prefered_endtime',
            'prefered_days', 'education', 'certification', 'identity', 'status',
            'resources', 'sessions'
        )
        exclude = ('id',)
        
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
