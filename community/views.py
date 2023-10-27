from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

# Create your views here.

class CreateCommunityApiView(generics.CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def post(self,request):
        mail=request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        serializer = self.serializer_class(data = request.data)
        if user.role.lower() == 'mentor':
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"user is not a mentor"},status=status.HTTP_403_FORBIDDEN)

class ListCommunityApiView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    
    def get(self, request):
        mail = request.user.email
        user = get_object_or_404(CustomUser, email=mail)
        
        communities = Community.objects.all()
        
        community_data = []
        
        for community in communities:
            # Get all members of the community and their images
            members = Members.objects.filter(community=community)
            user_images = [member.user.image for member in members]

            data = CommunitySerializer(community).data
            community_data.append({
                "community": data,
                "user_images": user_images
            })

        response = {
            "community_data": community_data
        }
        return Response(response, status=status.HTTP_200_OK)
    
class RetrieveCommunityApiView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = "id"
    
    def get(self, request, *args, **kwargs):
        mail = request.user.email
        user = get_object_or_404(CustomUser, email=mail)
        id = kwargs.get("id")
        if id:
            community = get_object_or_404(Community, id=id)
            
            user_image = None
            if member := Members.objects.filter(community=community).first():
                user_image = member.user.image

            data = CommunitySerializer(community, many=False).data
            response = {
                "image": user_image,
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK) 

       
class JoinCommunityApiView(generics.CreateAPIView):
    queryset = Members.objects.all()
    serializer_class = MembersSerializer

    allowed_methods = ['POST']  # Allow only POST requests

    def post(self, request, communityid, *args, **kwargs):
        mail = request.user.email
        user = get_object_or_404(CustomUser, email=mail)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                community_instance = Community.objects.get(id=communityid)
                serializer.save(community=community_instance,user = user )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Community.DoesNotExist:
                return Response({'detail': 'Community not found.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
