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
    

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested serialization of Category
    class Meta:
        model = Resource
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    company = CompanySerializer() 
    industry = IndustrySerializer()  
    skills = SkillSerializer()  
    education = EducationSerializer()
    certification = CertificationSerializer()

    class Meta:
        model = Mentor 
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user

            validated_data['user'] = user
        
        company_id = validated_data.pop('company')
        industry_id = validated_data.pop('industry')
        skills_id = validated_data.pop('skills')
        education_id = validated_data.pop('education')
        certification_id = validated_data.pop('certification')
        # identity_id = validated_data.pop('identity')
        # resources_id = validated_data.pop('resources')
        # sessions_id = validated_data.pop('sessions')

        mentor = Mentor.objects.create(**validated_data)

        # mentor.user_id = user
        # mentor.company_id = company_id
        # mentor.industry_id = industry_id
        # mentor.skills_id = skills_id
        # mentor.education_id = education_id
        # mentor.certification_id = certification_id
        # # mentor.identity_id = identity_id
        # # mentor.resources_id = resources_id
        # # mentor.sessions_id = sessions_id

        return mentor
