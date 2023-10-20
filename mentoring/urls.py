from django.urls import path
from .views import MentorCreationView
from .views import MentorSessionList
from django.urls import include, path
from . import views
from .Mentee import get

urlpatterns=[
    path('mentors/all',views.AllMentorsView.as_view(),name='mentor-all'),
    path('mentee/all',views.AllMenteeView.as_view(),name='mentee-all'),
    path("mentee/<str:pk>/", get.MenteeDetail.as_view(), name='mentee-detail'),
    path('<str:id>/mentor-update',views.UpdateMentorView.as_view(),name='mentor-update'),
    path('<str:id>/mentee-update',views.UpdateMenteeView.as_view(),name='mentee-update'),
    path('profile/',views.GetloggedUserView.as_view(),name='log-profile'),
    path('sessions/mentor/<str:mentor_id>/', views.MentorSessionList.as_view(), name='mentor-session-list'),
    path("session/create/", views.SessionCreateAPIView.as_view()),
    path("category/", views.CategoryListCreateAPIView.as_view()),
    path('sessions/mentor/<str:mentor_id>/', views.MentorSessionList.as_view(), name='mentor-session-list'),
    path("create-mentee-profile/", views.MenteeCreateAPIView.as_view()),
    path("create-company/", views.CompanyListCreateAPIView.as_view()),
    path("skill/", views.SkillListCreateAPIView.as_view()),
    path('create-mentor-profile/', MentorCreationView.as_view(), name='create-user-data'),
    path('mentor/<str:id>/',views.GetMentorApiView.as_view(),name='Get_all_mentor_by_id'),
    path('v1/searching/<str:search_term>', views.SearchResourcesApiView.as_view(), name='resouce-search'),
]
