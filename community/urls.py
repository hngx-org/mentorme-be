from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('communities/', views.CreateCommunityApiView.as_view(), name='community-create'),
    path('communities/all/', views.ListCommunityApiView.as_view(), name='communities-list'),
    path('communities/<str:id>/', views.RetrieveCommunityApiView.as_view(), name='communities-retrieve'),
    path('communities/join/<str:communityid>/', views.JoinCommunityApiView.as_view(), name='community-join'),
]