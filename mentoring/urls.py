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
    path('mentor/<str:pk>/',get.GetMentorApiView.as_view(),name='Get_all_mentor_by_id'),
    path('user-update',views.UpdateUserView.as_view(),name='user-update'),
    path('profile/',views.GetloggedUserView.as_view(),name='log-profile'),
    # path("session/create/", views.SessionCreateAPIView.as_view()),
    path("category/", views.CategoryListCreateAPIView.as_view()),
    path('sessions/mentor/<str:mentor_id>/', views.MentorSessionList.as_view(), name='mentor-session-list'),
    path("create-mentee-profile/", views.MenteeCreateAPIView.as_view()),
    path("create-company/", views.CompanyListCreateAPIView.as_view()),
    path("skill/", views.SkillListCreateAPIView.as_view()),
    path('create-mentor-profile/', MentorCreationView.as_view(), name='create-user-data'),
    path('resource/searching/<str:search_term>/', views.SearchResourcesApiView.as_view(), name='resource-search'),
    path('resource/filter/<str:category>/', views.FilterResourceByCategory.as_view() , name='resource-filter'),
    path('resource/user/', views.GetUserResource.as_view(), name='user-resource'),
    path('resource/create/', views.CreateResourceApiView.as_view(), name='resource-create'),
    path('resource/', views.ListResourceApiView.as_view(), name='resouce-list'),
    path('resource/<str:id>', views.RetrieveResourceApiView.as_view(), name='resource-detail'),
    path('resource/update/<str:id>/', views.updateResourceApiView.as_view(), name='resource-update'),
    path('resource/<str:id>/', views.DeleteResourceApiView.as_view(), name='resource-delete'),
    
    
    path('sessions/create-free-session/', views.FreeSessionCreateView.as_view(), name='create-free-session'),
    path('sessions/create-oneoff-session/', views.OneOffSessionCreateView.as_view(), name='create-oneoff-session'),
    path('sessions/create-recurring-session/', views.RecurringSessionCreateView.as_view(), name='create-recurring-session'),
    path('sessions/mentee/book-session/', views.SessionBookingCreateView.as_view(), name='book-session'),
    path('sessions/mentee/upcoming/<str:mentee_id>/', views.UpcomingSessionsByMentee.as_view(), name='upcoming-sessions-by-mentee'),
    path('sessions/all/',views.AllSessionsView.as_view(),name='sessions'),
    path('sessions/free/',views.FreeSessionsView.as_view(),name='sessions'),
    path('sessions/oneoff',views.OneOffSessionsView.as_view(),name='sessions'),
    path('sessions/recurring/',views.RecurringSessionsView.as_view(),name='sessions'),
    path('sessions/mentor/upcoming/<str:mentor_id>/', views.UpcomingSessionsForMentor.as_view(), name='upcoming-sessions-for-mentor'),
    path('sessions/mentor/<str:mentor_id>/', views.MentorSessionList.as_view(), name='mentor-session-list'),
    path('sessions/mentee/<str:mentee_id>/', views.MenteeSessionList.as_view(), name='mentee-session-list'),
    path('sessions/<uuid:pk>/', views.SessionUpdateView.as_view(), name='session-update'),
    path('sessions/<uuid:pk>/delete', views.SessionDeleteView.as_view(), name='session-delete'),



]
