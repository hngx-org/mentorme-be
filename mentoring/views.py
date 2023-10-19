from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .serializers import MentorProfileSerializer
from .models import *
from rest_framework.permissions import IsAuthenticated


class MentorCreationView(APIView):
    def get(self, request):
        mentors = Mentor.objects.all()
        serializer = MentorProfileSerializer(mentors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MentorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
