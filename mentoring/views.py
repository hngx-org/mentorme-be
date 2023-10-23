from django.utils import timezone
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
from django.db.models import Q
from rest_framework.views import APIView


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
            'mentor': mentor_serializer.data
        }, status=status.HTTP_201_CREATED)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetMentorApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset= Mentor.objects.all()
    serializer_class= MentorProfileAllSerializer
    lookup_field = "id"
    

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
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
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
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
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
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
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
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
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=Mentor.objects.all()
    serializer_class=MentorProfileAllSerializer

class AllMenteeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=Mentee.objects.all()
    serializer_class=MenteeProfileAllSerializer

class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=Mentee.objects.all()
    serializer_class=MenteeDetailsSerializer

    def put(self, request, *args, **kwargs):
        user=request.user
        if user.role == "mentee":
            instance= get_object_or_404(Mentee,user=user)
            serializer=self.serializer_class(instance,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        instance=get_object_or_404(Mentor,user=user)
        serializer=MentorDetailsSerializer(instance,data=request.data)
        if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

    
    
class GetloggedUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=CustomUser.objects.all()
    serializer_class=MenteeDetailsSerializer
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, *args, **kwargs):
        mail=request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        if user.role.lower() == 'mentor':
            mentor=get_object_or_404(Mentor,user=user)
            serializer=MentorDetailsSerializer(mentor)
            return Response(serializer.data,status=status.HTTP_200_OK)
        mentee=get_object_or_404(Mentee,user=user)
        serializer=self.serializer_class(mentee)
        return Response(serializer.data,status=status.HTTP_200_OK)    
    
class SearchResourcesApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    def get(self, request, search_term):
         
        try:
            # Use Q objects to search multiple fields with an OR condition
            querysets = Resource.objects.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
            if not querysets.exists():
                return Response(
                    {"Message": f"No resource containing '{search_term}' found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except:    
             return Response({"error": "no result"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(querysets, many=True)
        return Response(serializer.data)
    
class CreateResourceApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedMentor]  # Add authentication to ensure the user is logged in.
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    def post(self,request,*args,**kwargs):
        mail=request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        serializer = ResourceSerializer(data=request.data)
        if user.role.lower() == 'mentor':
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"user is not a mentor"},status=status.HTTP_403_FORBIDDEN)
    
class ListResourceApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class RetrieveResourceApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = "id"

class updateResourceApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = "id"
    
    def perform_update(self, serializer):
        mail=self.request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        resource = self.get_object()
        if resource.user != user:
            return Response({"detail":"you no allowed to update this Resource"},status=status.HTTP_403_FORBIDDEN)
        if user.role.lower() == 'mentor':
            serializer.save()
            return Response({"message": "Resource updated successfully."}, status=status.HTTP_200_OK)
        return Response({"detail":"user is not a mentor"},status=status.HTTP_403_FORBIDDEN)
 

class DeleteResourceApiView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = "id"

    def perform_destroy(self, instance):
        mail=self.request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        resource = self.get_object()
        if resource.user != user:
            return Response({"detail":"you no allowed to update this Resource"},status=status.HTTP_403_FORBIDDEN)
        if user.role.lower() == 'mentor':
            super().perform_destroy(instance)
            return Response({"message": "Resource deleted successfully."}, status=status.HTTP_204_NO_CONTENT )
        return Response({"detail":"user is not a mentor"},status=status.HTTP_403_FORBIDDEN)

class GetUserResource(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    serializer_class = ResourceSerializer
    
    def get(self,request,*args,**kwargs):
        mail=self.request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        try:
            if user.role.lower() != 'mentor':
                return Response({"detail":"user is not a mentor"},status=status.HTTP_403_FORBIDDEN)
            created_resources = Resource.objects.filter(user=user)
            serializer = ResourceSerializer(created_resources,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except created_resources is None:
            return Response({"detail":"you have not created any resource"},status=status.HTTP_200_OK)


class FilterResourceByCategory(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    serializer_class = ResourceSerializer
    
    def get(self,request,category,*args,**kwargs):
        try:
            categorized_resources = Resource.objects.filter(category=category)
            serializer = ResourceSerializer(categorized_resources,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except categorized_resources is None:
            return Response({"detail":"no resources in this category"}, status=status.HTTP_200_OK)
    
    
class AllSessionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    serializer_class = SessionSerializer

    def get_queryset(self):
        return Session.objects.all()


class FreeSessionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=Session.objects.filter(type_of_session='f')
    serializer_class=FreeSessionSerializer
    
class OneOffSessionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=Session.objects.filter(type_of_session='o')
    serializer_class=OneOffSessionSerializer
    
class RecurringSessionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add authentication to ensure the user is logged in.
    queryset=Session.objects.filter(type_of_session='r')
    serializer_class=RecurringSessionSerializer

class FreeSessionCreateView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = FreeSessionSerializer
    permission_classes = [IsAuthenticatedMentor]  # You can add more specific permissions here

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OneOffSessionCreateView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = OneOffSessionSerializer
    permission_classes = [IsAuthenticatedMentor]  # You can add more specific permissions here

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RecurringSessionCreateView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = RecurringSessionSerializer
    permission_classes = [IsAuthenticatedMentor]  # You can add more specific permissions here

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SessionBookingCreateView(generics.CreateAPIView):
    queryset = SessionBooking.objects.all()
    serializer_class = SessionBookingSerializer
    permission_classes = [IsAuthenticatedMentee]  # You can add more specific permissions here

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UpcomingSessionsByMentee(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedMentee]  # Add authentication to ensure the user is logged in.

    def get_queryset(self):
        mentee_id = self.kwargs['mentee_id'] 
        return Session.objects.filter(sessionbooking__mentee_id=mentee_id, start_date__gte=timezone.now()).order_by('start_date')

class UpcomingSessionsForMentor(generics.ListAPIView):
    permission_classes = [IsAuthenticatedMentor]  # Add authentication to ensure the user is logged in.
    serializer_class = SessionSerializer

    def get_queryset(self):
        mentor_id = self.kwargs['mentor_id']
        return Session.objects.filter(mentor_id=mentor_id, start_date__gte=timezone.now()).order_by('start_date')

class MentorSessionList(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedMentor]  # Add authentication to ensure the user is logged in.

    def get_queryset(self):
        mentor_id = self.kwargs.get('mentor_id')
        try:
            mentor = Mentor.objects.get(id=mentor_id)
            return Session.objects.filter(mentor=mentor)
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


class MenteeSessionList(generics.ListAPIView):
    serializer_class = SessionBookingSerializer
    permission_classes = [IsAuthenticatedMentee]  # Add authentication to ensure the user is logged in.


    def get_queryset(self):
        mentee_id = self.kwargs.get('mentee_id')
        try:
            mentee = Mentee.objects.get(id=mentee_id)
            return SessionBooking.objects.filter(mentee=mentee)
        except Mentee.DoesNotExist:
            return SessionBooking.objects.none()
            
class SessionUpdateView(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedMentor]  # Add authentication to ensure the user is logged in.


class SessionDeleteView(generics.DestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedMentor]  # Add authentication to ensure the user is logged in.


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
