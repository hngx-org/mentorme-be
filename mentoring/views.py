from django.shortcuts import render
from rest_framework import generics
from .serializers import MentorProfileAllSerializer,MenteeProfileAllSerializer,UserlogSerializer
# Create your views here.
from .models import Mentor,Mentee,CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
class AllMentorsView(generics.ListAPIView):
    queryset=Mentor.objects.all()
    serializer_class=MentorProfileAllSerializer

class AllMenteeView(generics.ListAPIView):
    queryset=Mentee.objects.all()
    serializer_class=MenteeProfileAllSerializer

class UpdateMentorView(generics.UpdateAPIView):
    queryset=Mentor.objects.all()
    serializer_class=MentorProfileAllSerializer
    lookup_field='id'

    def put(self, request, *args, **kwargs):
        instance=self.get_object()
        if request.user == instance:
            serializer=self.serializer_class(data=instance)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'You\'re not allowed to update another persons profile'}, status=status.HTTP_403_FORBIDDEN)

class UpdateMenteeView(generics.UpdateAPIView):
    queryset=Mentee.objects.all()
    serializer_class=MenteeProfileAllSerializer
    lookup_field='id'

    def put(self, request, *args, **kwargs):
        instance=self.get_object()
        if request.user == instance:
            serializer=self.serializer_class(data=instance)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'You\'re not allowed to update another persons profile'}, status=status.HTTP_403_FORBIDDEN)
class GetloggedUserView(generics.RetrieveAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserlogSerializer
    def retrieve(self, request, *args, **kwargs):
        # permission_classes=[IsAuthenticated]
        user=request.user.email
        response=get_object_or_404(CustomUser,email=user)
        serializer=self.serializer_class(response)
        return Response(serializer.data,status=status.HTTP_200_OK)
    