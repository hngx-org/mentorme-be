from django.urls import path
from .views import MentorSessionList

urlpatterns = [
    path('sessions/mentor/<str:mentor_id>/', MentorSessionList.as_view(), name='mentor-session-list'),
]