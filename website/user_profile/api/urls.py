from django.urls import path

from .views import (
    RegistrationView,
    # ProfileRegistrationView,
    ListProfileView,
    RetrieveUpdateProfileView,
    UserSearchView,
    username_existence_check,
    email_existence_check,
    username_existence_check,
    email_existence_check,
    GetProfileRoleView,
    RequestPasswordResetAPI,
    ResetPasswordConfirmAPI,
)
from user_profile.views import activate

app_name = 'user_profile_api'

urlpatterns = [
    # Profile related(except first)
    path('register/', RegistrationView.as_view(), name='user_registration'),
    path('', ListProfileView.as_view(), name='all_users_list'),
    # path('resend-user-activation/', resendVerificationView, name='resend-user-activation'),
    
    # Password Reset
    path('password-reset/', RequestPasswordResetAPI.as_view(), name='password_reset_api'),
    path('password-reset-confirm/', ResetPasswordConfirmAPI.as_view(), name='password_reset_confirm_api'),
    
    # Specific Checks and Views
    path('search', UserSearchView.as_view(), name='user_search'),
    path('username-check', username_existence_check, name='username_exists'),
    path('email-check', email_existence_check, name='email_exists'),
    path('roles', GetProfileRoleView.as_view(), name='roles'),
    
    # Account Activation
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),

    # Profile Detail (Catch-all)
    path('<str:username>/', RetrieveUpdateProfileView.as_view(), name='user_detail'),
]
