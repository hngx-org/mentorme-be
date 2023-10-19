from django.urls import path
from .views import MenteeCreateView

urlpatterns = [
    path('create-mentee-profile/', MenteeCreateView.as_view(), name='create_mentee'),
]