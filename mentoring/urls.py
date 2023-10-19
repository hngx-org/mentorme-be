from django.urls import path
from .views import MentorCreationView
from .views import MentorSessionList

urlpatterns = [
    path('create_mentor_data/', MentorCreationView.as_view(), name='create-user-data'),
    path('sessions/mentor/<str:mentor_id>/', MentorSessionList.as_view(), name='mentor-session-list'),
]


