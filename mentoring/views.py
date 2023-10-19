from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Mentee
from users.models import CustomUser
from .serializers import MenteeSerializer, UserSerializer

# Create your views here.
class MenteeCreateView(generics.CreateAPIView):
    """view for creating a mentee profile"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Extract user data that wasn't used during user creation
        remaining_data = {
            key: value for key, value in request.data.items()
            if key not in user_serializer.Meta.fields
        }

        mentee_data = request.data.get('mentee_data', {})  # Extract mentee-specific data
        mentee_data.update(remaining_data)  # Add remaining data to the mentee data
        mentee_data['user'] = user.id  # Associate the user with the mentee

        mentee_serializer = MenteeSerializer(data=mentee_data)
        mentee_serializer.is_valid(raise_exception=True)
        mentee = mentee_serializer.save()

        return Response({
            'user': user_serializer.data,
            'mentee': mentee_serializer.data
        }, status=status.HTTP_201_CREATED)