from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.serializers import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from user_profile.models import Profile
from user_profile.utils import send_verification_mail
from user_profile.utils_permissions import ViewUpdatePermission
from user_profile.utils import ProfileMatcher

import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.files.base import ContentFile


from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    UserSerializer,
    ProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from user_profile.tokens import password_reset_token
from django.template.loader import render_to_string



# TODO
# 1) Email verification and resend email verification

# For customised tokens. Don't use if not needed
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # data['isStudent'] = self.user.groups.first().name == 'student'
        # data['user'] = UserSerializer(self.user).data
        return data


# Google Login api handler
class LoginWithGoogleView(APIView):

    def generate_token(self,user):
        refresh = RefreshToken.for_user(user)

        refresh['email'] = user.email

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        access_token = request.data.get('token')
        GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID", None)
        if not GOOGLE_CLIENT_ID:
            GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", None)

        try:
            TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=" + access_token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            token_info = requests.get(TOKEN_INFO_URL, data={}, headers=headers).json()
            
            if 'error' in token_info:
                print(f"Google API Error: {token_info}")
                return Response(data={'response': 'Invalid token from Google'}, status=400)

            if token_info['issued_to'] == GOOGLE_CLIENT_ID:
                try:
                    USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + access_token
                    user_info = requests.get(USER_INFO_URL, data={}, headers=headers).json()
                    user, created = User.objects.get_or_create(
                        username=user_info['email'].split('@')[0],
                        defaults={
                            'first_name': user_info.get('name', ''),
                            'last_name': user_info.get('given_name', ''),
                            'email': user_info['email']
                        }
                    )
                    
                    if created:
                        try:
                            profile = user.profile
                            profile.name = user_info.get('name', '')
                            picture_url = user_info.get('picture')
                            if picture_url:
                                image_response = requests.get(picture_url)
                                if image_response.status_code == 200:
                                    profile.image.save(f"{user.username}_google.jpg", ContentFile(image_response.content), save=False)
                            profile.save()
                        except Exception as e:
                            print(f"Error saving user profile data from Google: {e}")

                    tokens = self.generate_token(user)
                    return Response(data={'access': tokens['access'], 'refresh': tokens['refresh'], 'response': 'valid', 'is_new_user': created}, status=200)
                except Exception as e:
                    print(f"User creation/retrieval error: {e}")
                    return Response(data={'response': 'Unauthorized'}, status=401)
            else:
                print(f"Client ID mismatch. Expected: {GOOGLE_CLIENT_ID}, Got: {token_info.get('issued_to')}")
                return Response(data={'response': 'Unauthorized - Client ID mismatch'}, status=401)
        except Exception as e:
            print(f"Top level error in LoginWithGoogleView: {e}")
            return Response(data={'response': 'Invalid token'}, status=400)



# For Getting The Role of the User
class GetProfileRoleView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            return Response(data={'role': profile.role}, status=200)
        except Exception as e:
            print(e)
            return Response(data={'response': 'Unauthorized'}, status=401)


# For customised tokens. Don't use if not needed
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        # is_active set to false in save method of the serializer
        user = serializer.save()
        domain = get_current_site(self.request).domain
        _ = send_verification_mail(domain=domain, user=user)
        # auto creation of profile done in model signal


class ListProfileView(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class RetrieveUpdateProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ViewUpdatePermission,)
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'

    def get_queryset(self):
        return Profile.objects.all()


class UserSearchView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('query')
        qs = Profile.objects.all()
        if not search_query:  # returns all profiles in case of empty query
            return qs
        matcher = ProfileMatcher(query=search_query)
        # using generator to save on space
        unsorted_matches = ((matcher.matcher(i), i) for i in qs if matcher.matcher(i) >= 0.5)
        return [i[1] for i in sorted(unsorted_matches, key=lambda x: x[0], reverse=True)]


@api_view(['GET', ])
def username_existence_check(request):
    search_query = request.query_params.get('username')
    if (not search_query) or (not User.objects.filter(username=search_query).exists()):
        return Response(data={'response': 'Username is available!', 'exists': 0})
    return Response(data={'response': 'Username already exists!', 'exists': 1})


@api_view(['GET', ])
def email_existence_check(request):
    search_query = request.query_params.get('email')
    if (not search_query) or (not User.objects.filter(email=search_query.lower()).exists()):
        return Response(data={'response': 'Email ID is not used yet!', 'exists': 0})
    return Response(data={'response': 'An account is registered with the email address!', 'exists': 1})


class RequestPasswordResetAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Logic from existing view
            current_site = get_current_site(request)
            subject = 'Reset Your RECursion Account Password'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token.make_token(user)
            
            # Using specific frontend URL construction
            frontend_base = settings.FRONTEND_BASE_URL
            
            # Send email
            # We reuse the template but ensure it uses the frontend link
            # Or we can just send the link directly if the template allows
            # The existing template likely uses 'uid' and 'token' to build a link.
            # We should check if the template uses 'frontend_base_url' correctly.
            
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'frontend_base_url': frontend_base, 
            })
            user.email_user(subject, message)
            
            return Response({"success": True, "message": "Password reset email sent."})
        return Response(serializer.errors, status=400)


class ResetPasswordConfirmAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({"error": "Invalid UID"}, status=400)

            if user is not None and password_reset_token.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({"success": True, "message": "Password has been reset."})
            else:
                return Response({"error": "Invalid or expired token"}, status=400)
                
        return Response(serializer.errors, status=400)
