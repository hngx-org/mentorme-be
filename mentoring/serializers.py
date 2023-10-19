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
    
from rest_framework import serializers
class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and isinstance(request.user, CustomUser):
            user_id = request.user.id

            education_data = validated_data.pop('education')
            company_data = validated_data.pop('company')
            industry_data = validated_data.pop('industry')
            skill_data = validated_data.pop('skill')
            session_data = validated_data.pop('session')
            identity_data = validated_data.pop('identity')
            certification_data = validated_data.pop('certification')
            resource_data = validated_data.pop('resource')

            education, created = Education.objects.get_or_create(**education_data)
            company_t, created = Company.objects.get_or_create(**company_data)
            industry, created = Industry.objects.get_or_create(**industry_data)
            skill, created = Skill.objects.get_or_create(**skill_data)
            session, created = Session.objects.get_or_create(**session_data)
            identity, created = Identity.objects.get_or_create(**identity_data)
            certification, created = Certification.objects.get_or_create(**certification_data)
            resource, created = Resource.objects.get_or_create(**resource_data)

            mentor = Mentor.objects.create(
                user_id=user_id,
                education=education.id,
                company_=company_t.id,
                industry=industry.id,
                skill=skill.id,
                session=session.id,
                identity=identity.id,
                certification=certification.id,
                resource=resource.id,
                **validated_data
            )

            return mentor
        else:
            raise serializers.ValidationError("Only authenticated CustomUser can create a Mentor.")
        return mentor

from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
