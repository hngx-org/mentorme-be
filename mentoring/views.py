from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *

class MentorCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def perform_create(self, serializer):
        user = self.request.user  
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        if isinstance(request.user, CustomUser):
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Only authenticated CustomUser can create a Mentor."},
                status=status.HTTP_403_FORBIDDEN
            )

class MentorSessionList(generics.ListAPIView):
    serializer_class = SessionSerializer

    def get_queryset(self):
        mentor_id = self.kwargs.get('mentor_id')
        try:
            sessions = Session.objects.filter(mentor__user__id=mentor_id)
            return sessions
        except Session.DoesNotExist:
            return Response(
                {"error": "No sessions found for the specified mentor."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
