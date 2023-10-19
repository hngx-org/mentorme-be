from django.urls import include, path
from . import views

urlpatterns=[
    path('mentors/all',views.AllMentorsView.as_view(),name='mentor-all'),
    path('mentee/all',views.AllMenteeView.as_view(),name='mentee-all'),
    path('<str:id>/mentor-update',views.UpdateMentorView.as_view(),name='mentor-update'),
    path('<str:id>/mentee-update',views.UpdateMenteeView.as_view(),name='mentee-update'),
    path('profile/',views.GetloggedUserView.as_view(),name='log-profile'),
    path('sessions/mentor/<str:mentor_id>/', views.MentorSessionList.as_view(), name='mentor-session-list'),
    path("session/create/", views.SessionCreateAPIView.as_view()),
    path("category/", views.CategoryListCreateAPIView.as_view()),
]
