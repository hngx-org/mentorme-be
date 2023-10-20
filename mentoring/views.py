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
from datetime import datetime
from django.core    .exceptions import ValidationError


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


class SessionMentorRetrieveAPIView(generics.RetrieveAPIView):
    """Retrieves all upcoming sessions of a mentor (POV: Mentor)"""
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get(self, request, *args, **kwargs):
        try:
            mentor = Mentor.objects.get(user=request.user)
        except (Mentor.DoesNotExist, ValidationError):
            return Response({"detail": "Not a mentor"},
                            status=status.HTTP_403_FORBIDDEN)
        qs = self.get_queryset()
        today = datetime.now().date
        sessions = self.serializer_class(qs.filter(mentor=mentor,
                                                   start_date_gte=today),
                                         many=True)
        return Response(sessions.data)


class SessMentorBookedRetrieveAPIView(generics.RetrieveAPIView):
    """Retrieves all upcoming booked sessions of a mentor (POV: Mentor)"""
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get(self, request, *args, **kwargs):
        try:
            mentor = Mentor.objects.get(user=request.user)
        except (Mentor.DoesNotExist, ValidationError):
            return Response({"detail": "Not a mentor"},
                            status=status.HTTP_403_FORBIDDEN)
        qs = self.get_queryset()
        today = datetime.now().date
        query = qs.filter(mentor=mentor,
                          start_date_gte=today).exclude(mentee=None)
        sessions = self.serializer_class(query, many=True)
        return Response(sessions.data)


class SessionRetrieveAPIView(generics.RetrieveAPIView):
    """Retrieves all free upcoming sessions of a mentor (POV: Mentee)"""
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get(self, request, mentor_id, *args, **kwargs):
        try:
            mentor = Mentor.objects.get(id=mentor_id)
        except (Mentor.DoesNotExist, ValidationError):
            return Response({"detail": "Mentor Does Exist"},
                            status=status.HTTP_404_NOT_FOUND)

        qs = self.get_queryset()
        today = datetime.now().date
        query = qs.filter(mentor=mentor,
                          mentee=None,
                          start_date_gte=today)
        sessions = self.serializer_class(query, many=True)
        return Response(sessions.data)


class SessionBookUpdateAPIView(generics.GenericAPIView):
    """Books a session of a mentor (POV: Mentee)"""
    queryset = Session.objects.all()

    def get_serializer(self):
        return None

    def get_serializer_class(self):
        return None

    def put(self, request, session_id, *args, **kwargs):
        try:
            session = Session.objects.get(id=session_id)
        except (Session.DoesNotExist, ValidationError):
            return Response({"detail": "Session ID is incorrect"},
                            status=status.HTTP_404_NOT_FOUND)
        if session.mentee:
            return Response({"detail": "Session was booked by another user"},
                            status=status.HTTP_409_CONFLICT)
        try:
            mentee = Mentee.objects.get(user=request.user)
        except (Mentee.DoesNotExist, ValidationError):
            return Response({"detail": "Not a mentee"},
                            status=status.HTTP_403_FORBIDDEN)
        session.mentee = mentee
        session.save()
        return Response(SessionSerializer(session).data)


class SessMenteeBookedRetrieveAPIView(generics.RetrieveAPIView):
    """Retrieves all upcoming booked sessions of a mentee (POV: Mentee)"""
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get(self, request, *args, **kwargs):
        try:
            mentee = Mentee.objects.get(user=request.user)
        except (Mentee.DoesNotExist, ValidationError):
            return Response({"detail": "Not a mentee"},
                            status=status.HTTP_403_FORBIDDEN)

        qs = self.get_queryset()
        today = datetime.now().date
        query = qs.filter(mentee=mentee,
                          start_date_gte=today)
        sessions = self.serializer_class(query, many=True)
        return Response(sessions.data)


class SessMenteeCanceledRetrieveAPIView(generics.GenericAPIView):
    """Retrieves all canceled booked sessions of a mentee (POV: Mentee)"""

    def get_serializer_class(self):
        return None

    def get_serializer(self):
        return None


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


class GetMentorApiView(generics.RetrieveAPIView):
    queryset= Mentor.objects.all()
    serializer_class= MentorProfileAllSerializer
    lookup_field = "id"


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
    serializer_class=MenteeDetailsSerializer
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, *args, **kwargs):
        mail=request.user.email
        user=get_object_or_404(CustomUser,email=mail)
        if user.role.lower() == 'mentor':
            serializer=MentorDetailsSerializer(user)
            response= serializer.data
            mentor=get_object_or_404(Mentor,user=user)
            response['skills']=mentor.skills
            return Response(response,status=status.HTTP_200_OK)
        serializer=self.serializer_class(user)
        response= serializer.data
        mentee=get_object_or_404(Mentee,user=user)
        response['expertise']=mentee.expertise
        return Response(response,status=status.HTTP_200_OK)

class SearchResourcesApiView(generics.ListAPIView):
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
                return Response({"Message":"No resource containing '{}' found!".format(search_term)}, status=status.HTTP_404_NOT_FOUND)
        except:
             return Response({"error": "no result"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(querysets, many=True)
        return Response(serializer.data)