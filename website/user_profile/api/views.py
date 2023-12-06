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

from user_profile.models import Profile
from user_profile.utils import send_verification_mail
from user_profile.utils_permissions import ViewUpdatePermission
from user_profile.utils import ProfileMatcher

import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
)


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
        try:
            TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v2/tokeninfo?access_token="+access_token
            headers = {
                "Authorization": "Bearer {access_token}",
               "Content-Type": "application/json"
            }
            token_info = requests.get(TOKEN_INFO_URL ,data = {} ,headers = headers).json()
            if token_info['issued_to'] == GOOGLE_CLIENT_ID:
                try:
                    USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo?access_token="+access_token
                    headers = {
                        "Authorization": "Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                    user_info = requests.get(USER_INFO_URL ,data = {} ,headers = headers).json()
                    user, created = User.objects.get_or_create(
                        username = user_info['email'].split('@')[0],
                        first_name = user_info['given_name'],
                        last_name = user_info['family_name'],
                        email = user_info['email']
                    )
                    tokens = self.generate_token(user)
                    return Response(data={'access': tokens['access'],'refresh':tokens['refresh'], 'response':'valid'}, status=200)
                except Exception as e:
                    print(e)
                    return Response(data={'response': 'Unauthorized'}, status=401)
            else:
                return Response(data={'response': 'Unauthorized'}, status=401)
        except Exception as e:
            print(e)
            return Response(data={'response': 'Invalid token'}, status=400)



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
