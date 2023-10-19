from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        user = CustomUser(
          email=validated_data['email'],
          first_name=validated_data['first_name'],
          last_name=validated_data['last_name'],
          role=validated_data['role']
          )
        user.set_password(validated_data['password'])
        user.is_complete = False
        user.is_active = False  
        user.email_verified = False  
    
        
    
        user.save()
        return user



class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is yet to be activated',
        'invalid_credentials': 'Invalid email or password'
    }


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'gender', 'bio', 'country', 'image']