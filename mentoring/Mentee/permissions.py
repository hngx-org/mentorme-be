from rest_framework import permissions
from mentoring.models import Mentee, Mentor
from mentoring.serializers import MenteeSerializer, MentorSerializer

class CanGetMentorOrMentee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Mentee):
            return obj.mentor == request.user or obj == request.user
        elif isinstance(obj, Mentor):
            return obj == request.user
        return False