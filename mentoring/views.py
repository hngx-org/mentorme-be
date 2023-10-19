from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .serializers import MentorProfileSerializer
from .models import *
from rest_framework.permissions import IsAuthenticated


class MentorCreationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.id

        mentor_data = request.data.get('mentor', {})
        mentor_data['user'] = user_id  
        
        required_fields = ['company', 'industry', 'education', 'certification', 'identity', 'resources', 'sessions']
        for field in required_fields:
            if field not in mentor_data:
                return Response({field: ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)


        serializer = MentorProfileSerializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            # Update or create mentor instance based on the user ID
            mentor, created = Mentor.objects.update_or_create(
                user_id=user_id,
                defaults=mentor_data
            )

            # Return success response if the data is created or updated successfully
            return Response({'message': 'Data created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Return error response with validation errors if the serializer data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics
from .models import Mentor
from .serializers import MentorSerializer

class MentorCreateView(generics.CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
