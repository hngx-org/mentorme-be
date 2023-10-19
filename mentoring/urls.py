from django.urls import path
from .views import MentorCreationView

urlpatterns = [
    path('create_mentor_data/', MentorCreationView.as_view(), name='create-user-data'),
    # Add other URLs as needed
]
