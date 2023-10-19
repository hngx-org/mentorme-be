#restframework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

#django
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q


#local imports
from .serializers import RegisterSerializer, LoginSerializer, PassVerificationSerializer, PassResetSerializer, VerificationSerializer, ResendOTPSerializer
from .utils import EmailManager, generate_token, BaseResponse, abort
from .models import Tokens

import time
import random
from datetime import datetime

User = get_user_model()


class RegisterUser(generics.CreateAPIView):
    """
        Register new user, including sending an otp to email address of the user for verifiication
    """
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    

    def create(self, request, *args, **kwargs):
        """OTP Creation and sending"""
        
        token = generate_token()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save()
        
        # Get the serialized user data
        res_data = serializer.data
        try:
            """Send otp to sign up user"""
            
            EmailManager.send_mail(
                subject=f"MentorMe - Complete SignUp",
                recipients=[user_instance.email],
                template_name="user_invite.html",
                context={"user": user_instance.id, "token":token}
            )


            new_token = Tokens()
            new_token.email = user_instance.email
            new_token.action = 'register'
            new_token.token = token
            new_token.exp_date = time.time() + 300
            new_token.save()


        except Exception as error:
            print(error)
            response =  BaseResponse(str(error), None, 'Email failure').to_dict()
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        res = {"message": "Token sent!", "code": 200, "data": res_data}
        return Response(res, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    """View for handling user authentication.
    This view is responsible for authenticating a user using the provided email and password. If the provided
    credentials are valid, the view returns a response with the user's authentication token. If the credentials are
    invalid, the view returns a 400 Bad Request response with an error message indicating that the provided
    credentials are incorrect.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        try:

            serializer = self.get_serializer(data=request.data)

            try:
                email = serializer.initial_data['email']
                password = serializer.initial_data['password']
            except:
                raise AuthenticationFailed('Email and password required')

            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise AuthenticationFailed('Invalid email or password.')

                if not user.is_active:
                    raise AuthenticationFailed('Your account is not active.')
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid email or password.')

            #TODO: add a user serializer to return the user data
            response =  super().post(request, *args, **kwargs)

            responseData = {
                "Authorization": response.data,
            }
            response.data = BaseResponse(responseData, None, 'Login successful').to_dict()
            return Response(response.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return abort(401, (e.detail))


class PasswordResetRequestView(APIView):
    """
    View to request for an otp to reset password
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        

            
            token = str(random.randint(1000, 9999))
            # OTP token
            new_token = Tokens()
            new_token.email = email
            new_token.action = 'resetpassword'
            new_token.token = token
            new_token.exp_date = time.time() + 300
            new_token.save()
            try:
                """Send otp to sign up user"""
                EmailManager.send_mail(
                    subject=f"MentorMe - Reset Password",
                    recipients=[new_token.email],
                    template_name="user_reset_password.html",
                    context={"user": user.id, "token":token}
                )

            except Exception as error:
                print(error)
            
            data = {
                'Token': token
            }
            base_response = BaseResponse(None, None, 'Reset OTP sent to email')
            return Response(base_response.to_dict(), status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return abort(404, 'An account with this email does not exist.')
        

class PasswordResetConfirmView(APIView):
    """
    This view is used to verify a reset password token
    """
    authentication_classes = ()
    permission_classes = ()

    
    def post(self, request):
        serializer = PassVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_token = serializer.validated_data['verification_token']
        

        try:
            user = User.objects.get(email=email)
            #verify the token that was passed
            token = Tokens.objects.filter(Q(email=email) & Q(action='resetpassword')).order_by('-created_at')[:1].first()
            print(token)
            result = check_password(verification_token, token.token)
            if result == True and token.exp_date >= time.time():
                token.date_used = datetime.now()
                token.confirmed = True
                user.save()
                token.save()

                base_response = BaseResponse(None, None, 'Token verified successfully.')
                return Response(base_response.to_dict(), status=status.HTTP_200_OK)
                return Response({'success': 'Password reset successful.'}, status=status.HTTP_200_OK)
            elif result and token.exp_date < time.time():
                return abort(401, 'Expired  token')

            else:
                raise User.DoesNotExist

        except User.DoesNotExist:
            return abort(401, 'Invalid  token')


class PasswordResetView(APIView):
    """
    This view is used to reset a password
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = PassResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            #verify the token that was passed
            token = Tokens.objects.filter(Q(email=email) & Q(action='resetpassword')).order_by('-created_at')[:1].first()
            print(token)
            
            if token.confirmed:
                user.set_password(password)
                user.save()
                base_response = BaseResponse(None, None, 'Password reset successful.')
                return Response(base_response.to_dict(), status=status.HTTP_200_OK)
                return Response({'success': 'Password reset successful.'}, status=status.HTTP_200_OK)
            else:
                raise User.DoesNotExist

        except User.DoesNotExist:
            return abort(401, 'Invalid  token')



class VerifyEmailView(APIView):
    """
    This view verifies creating account with otp

    POST - takes the otp and the email to verify
    """
    
    permission_classes = ()

    @swagger_auto_schema(
        request_body=VerificationSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_description="Verify user email by taking in otp"
    )
    @action(detail=False, methods=['post'])
    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_token = serializer.validated_data['verification_token']

        try:
            user = User.objects.get(email=email)
            token = Tokens.objects.filter(Q(email=email) & Q(action='register')).order_by('-created_at')[:1].first()

            result = check_password(verification_token, token.token)
            if result == True and token.exp_date >= time.time():
                token.date_used = datetime.now()
                user.is_active = True
                user.email_verified = True
                user.save()
                token.save()

                exception = None
                try:
                    
                    print(user)
                    userserializer = RegisterSerializer(user)
                except Exception as e:
                    exception = e
                
                base_response = BaseResponse(data=userserializer.data, exception=exception, message='User successfully verified')
                return Response(base_response.to_dict(), status=status.HTTP_200_OK)
                
            elif result and token.exp_date < time.time():
                return abort(401, 'Token has expired')
            else:
                raise User.DoesNotExist

        except User.DoesNotExist:
            return abort(401, 'Invalid verification token')


class ResendOTPView(APIView):
    """Send a new otp to an unverify user upon request for another OTP 
        if the previous token has expired or not valid 
    """
    permission_classes = []
    

    @swagger_auto_schema(
        request_body=ResendOTPSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_description="Verify user email by taking in otp"
    )
    @action(detail=False, methods=['post'])
    def post(self, request):
        """
        Update the token table upon a new request for another otp
            get user email to verify if the email exist 
            
        """
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist as error:
            return abort(404, 'User with this email does not exist.')
            
        '''
        If email exist check if the email has been verified or not before proceeding to
        send a new otp to the user and update the token table
        '''
        token = generate_token()
        if not user.email_verified:
            existing_token = Tokens.objects.filter(email=email).first()
            if existing_token:
                    existing_token.token = token
                    existing_token.exp_date = time.time() + 300
                    existing_token.save()
            else:
                new_token_entry = Tokens(email=email, action='request', token=token, exp_date=time.time() + 300)
                new_token_entry.save()


            try:
                """Send otp to sign up user"""
                EmailManager.send_mail(
                    subject=f"MentorMe",
                    recipients=[email],
                    template_name="user_invite.html",
                    context={"user": user.id, "token":token}
                )

            except Exception as error:
                print(error)

        else:
            base_response = BaseResponse(data=email, exception=None, message='Email has been verified and can proceed to perform operation')
            return Response(base_response.to_dict(), status=status.HTTP_200_OK)
        
        return Response(BaseResponse(data=email, exception=None, message='OTP successfully sent').to_dict(), status=status.HTTP_200_OK)