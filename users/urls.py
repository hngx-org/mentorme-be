from django.urls import include, path
from rest_framework import routers
from .views import *


urlpatterns = [
    path('register', RegisterUser.as_view(), name="register"),
    path('verify-email', VerifyEmailView.as_view(), name='verify-email'),
    path('login', LoginView.as_view(), name="login-view"),
    #path('request-reset-password', PasswordResetRequestView.as_view(), name="reset-password"),
    #path('reset-password', PasswordResetConfirmView.as_view(), name="reset-password"),
    path('request-otp', ResendOTPView.as_view(), name='request-otp'),
    path(
        "reset_password/<str:uidb64>/<str:token>",
        ResetPassword.as_view(),
        name="reset_password",
    ),
    path(
        "forgot_password/<str:email>",
        SendResetPasswordEmail.as_view(),
        name="reset-password-email",
    ),


]

