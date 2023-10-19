from django.urls import path
from . import views


urlpatterns = [
    path("session/create/", views.SessionCreateAPIView.as_view()),
    path("category/", views.CategoryListCreateAPIView.as_view()),

]
