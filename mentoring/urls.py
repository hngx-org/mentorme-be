from django.urls import path
from . import views


urlpatterns = [
    path("session/create/", views.SessionCreateAPIView.as_view()),
    path("category/", views.CategoryListCreateAPIView.as_view()),
    path('sessions/mentor/<str:mentor_id>/', views.MentorSessionList.as_view(), name='mentor-session-list'),
    path("create-mentee-profile/", views.MenteeCreateAPIView.as_view()),
    path("create-company/", views.CompanyListCreateAPIView.as_view()),

]
