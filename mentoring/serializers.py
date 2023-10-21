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
    

from .models import Session, Category, Company, Industry, Mentee, Mentor

from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name','email', 'image', 'gender', 'bio', 'country')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


    def validate_bio(self, value):
        sql_injection_pattern = r'[;\'"]'
        if re.search(sql_injection_pattern, value):
            raise serializers.ValidationError("Bio contains potentially malicious content.")

        if len(value) > 250:
            raise serializers.ValidationError("Bio cannot exceed 250 characters.")

        return value


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
        exclude = ['identity', 'resources', 'status']
        
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
        
        certification, created = Certification.objects.get_or_create(**certification_id)
        industry, created = Industry.objects.get_or_create(**industry_id)
        skills, created = Skill.objects.get_or_create(**skills_id)
        company, created = Company.objects.get_or_create(**company_id)
        education, created = Education.objects.get_or_create(**education_id)
        
        validated_data['certification'] = certification
        validated_data['industry'] = industry        
        validated_data['skills'] = skills
        validated_data['company'] = company        
        validated_data['education'] = education

        mentor = Mentor.objects.create(**validated_data)


        return mentor
class MentorProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields='__all__'

class MenteeProfileAllSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model=Mentee
        fields='__all__'  
class MentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mentor
        fields=['job_title' , 'company' ,'industry', 
    'yearsofExp' ,
    'skills' ,
    'linkedin' ,
    'twitter' ,
    'other_links' ,
    'mentoring_exp',
    'mentoring_type',
    'availability',
    'prefered_time',
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






class MenteeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Mentee
        exclude = ['experience', 'links']


class MenteeDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Mentee
        fields = '__all__'


class MentorDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Mentor
        fields = '__all__'



class UserlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','image']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super(SessionSerializer, self).to_representation(instance)
        
        # Remove fields with None values
        data = {key: value for key, value in data.items() if value is not None}
        
        return data
        
class SessionBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionBooking
        fields = '__all__'
        
class FreeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'description', 'start_date', 'start_time', 'relevant_topics', 'mentor','attendees_limit', 'session_type', 'session_state', 'session_url', 'tag', 'duration', 'type_of_session']
        
class OneOffSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'description', 'start_date', 'start_time', 'relevant_topics', 'mentor','session_type', 'session_state', 'session_url', 'tag', 'duration','type_of_session']
        
class RecurringSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'description', 'start_date', 'start_time', 'relevant_topics', 'mentor','occurence', 'no_of_session', 'session_type', 'session_state', 'session_url', 'tag','type_of_session']