from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import IsAuthenticatedMentee, IsAuthenticatedMentor
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import UserSerializer
from users.utils import abort

class MentorCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedMentor]
    queryset = CustomUser.objects.all()
    serializer_class = MentorSerializer

    

    def create(self, request, *args, **kwargs):

        # Create a mentor object
        mentor_serializer = self.get_serializer(data=request.data)
        mentor_serializer.is_valid(raise_exception=True)
        mentor = mentor_serializer.save(user=request.user, status='Verified')

        # Update the user information
        user = request.user
        user_serializer = UserSerializer(data=request.data.get('user', {}), instance=user, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save(is_complete=True)

        return Response({
            'user': UserSerializer(user).data,
            'mentee': mentor_serializer.data
        }, status=status.HTTP_201_CREATED)

class SessionCreateAPIView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            mentor = Mentor.objects.get(user=request.user)
        except Mentor.DoesNotExist:
            return Response({"detail": "Not a mentor"},
                            status=403)
        serializer["mentor"] = mentor
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)


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



class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=201)



class IndustryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=201)


class SkillListCreateAPIView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=201)



class MenteeCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MenteeSerializer
    permission_classes = [IsAuthenticatedMentee]  # Add authentication to ensure the user is logged in.

    def create(self, request, *args, **kwargs):
        # Create a Mentee object
        mentee_serializer = self.get_serializer(data=request.data)
        mentee_serializer.is_valid(raise_exception=True)
        mentee = mentee_serializer.save(user=request.user)

        # Update the user information
        user = request.user
        user_serializer = UserSerializer(data=request.data.get('user', {}), instance=user, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save(is_complete=True)

        return Response({
            'user': UserSerializer(user).data,
            'mentee': mentee_serializer.data
        }, status=status.HTTP_201_CREATED)

      
        

class AllMentorsView(generics.ListAPIView):
    queryset=Mentor.objects.all()
    serializer_class=MentorProfileAllSerializer

class AllMenteeView(generics.ListAPIView):
    queryset=Mentee.objects.all()
    serializer_class=MenteeProfileAllSerializer

class UpdateMentorView(generics.UpdateAPIView):
    queryset=Mentor.objects.all()
    serializer_class=MentorUpdateSerializer
    lookup_field='id'

    def put(self, request, *args, **kwargs):
        instance=self.get_object()
        if request.user.email == instance.user.email:
            serializer=self.serializer_class(instance,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'You\'re not allowed to update another persons profile'}, status=status.HTTP_403_FORBIDDEN)

class UpdateMenteeView(generics.UpdateAPIView):
    queryset=Mentee.objects.all()
    serializer_class=MenteeUpdateSerializer
    lookup_field='id'

    def put(self, request, *args, **kwargs):
        instance=self.get_object()
        if request.user.email == instance.user.email:
            serializer=self.serializer_class(instance,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'You\'re not allowed to update another persons profile'}, status=status.HTTP_403_FORBIDDEN)
    
    
class GetloggedUserView(generics.RetrieveAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserlogSerializer
    def retrieve(self, request, *args, **kwargs):
        # permission_classes=[IsAuthenticated]
        mail=request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        if user.role.lower() == 'mentor':
            serializer=UserlogSerializer(user)
            response= serializer.data
            mentor=get_object_or_404(Mentor,user=user)
            response['skills']=mentor.skills
            return Response(response,status=status.HTTP_200_OK)
        serializer=self.serializer_class(user)
        response= serializer.data
        mentee=get_object_or_404(Mentee,user=user)
        response['expertise']=mentee.expertise
        return Response(response,status=status.HTTP_200_OK)    