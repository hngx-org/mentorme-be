from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from mentoring.models import Mentee, Mentor
from mentoring.serializers import MenteeSerializer, MentorSerializer

class MenteeDetail(generics.RetrieveAPIView):
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer

    def get_object(self):
        mentee_id_or_name = self.kwargs['pk']
        is_mentee = True

        if mentee_id_or_name.isdigit():
            obj = get_object_or_404(Mentee, id=mentee_id_or_name)
        else:
            obj = get_object_or_404(Mentee, title=mentee_id_or_name)

        if not is_mentee:
            try:
                obj = Mentor.objects.get(pk=mentee_id_or_name)
            except (ValueError, TypeError, Mentor.DoesNotExist):
                obj = get_object_or_404(Mentor, title=mentee_id_or_name)

            serializer = MentorSerializer(obj)
            return Response(serializer.data)

        serializer = MenteeSerializer(obj)
        return Response(serializer.data)
