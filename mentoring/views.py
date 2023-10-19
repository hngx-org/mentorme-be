from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Session
from .serializers import SessionSerializer


# Create your views here.
class SessionCreateAPIView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
