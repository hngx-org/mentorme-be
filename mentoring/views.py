from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import UserSerializer
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


# Create your views here.
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


class MenteeCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email=request.user.email)

        user.first_name = user_serializer.data['first_name']
        user.last_name = user_serializer.data['last_name']
        user.image = user_serializer.data['image']
        user.gender = user_serializer['gender']
        user.country = user_serializer['country']
        user.bio = user_serializer['bio']
        user.is_complete = True
        user.save()
        


        # Extract user data that wasn't used during user creation
        remaining_data = {
            key: value for key, value in request.data.items()
            if key not in user_serializer.Meta.fields
        }

        mentee_data = request.data.get('mentee_data', {})  # Extract mentee-specific data
        mentee_data.update(remaining_data)  # Add remaining data to the mentee data
        company = Company.objects.get(id=mentee_data['company'])
        mentee_data['company'] = company.id
        mentee_data['user'] = user.id

        mentee_serializer = MenteeSerializer(data=mentee_data)
        mentee_serializer.is_valid(raise_exception=True)
        mentee = mentee_serializer.save()

        return Response({
            'user': user_serializer.data,
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

