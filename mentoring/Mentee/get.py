from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from mentoring.models import Mentee, Mentor
from mentoring.serializers import MenteeProfileAllSerializer, MentorProfileAllSerializer
from .permissions import CanGetMentorOrMentee


class MenteeDetail(generics.RetrieveAPIView):
    queryset = Mentee.objects.all()
    serializer_class = MenteeProfileAllSerializer
    permission_classes = [CanGetMentorOrMentee]

    def get_object(self):
        mentee_id = self.kwargs['pk']
        obj = get_object_or_404(Mentee, id=mentee_id)
        return obj


class GetMentorApiView(generics.RetrieveAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorProfileAllSerializer
    permission_classes = [CanGetMentorOrMentee]

    def get_object(self):
        mentor_id = self.kwargs['pk'] # Check the value of mentor_id
        obj = Mentor.objects.get(id=mentor_id)
        return obj


