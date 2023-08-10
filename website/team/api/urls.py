from django.urls import path

from .views import (
    ListCreateMembersView,
)

app_name = 'team_api'

urlpatterns = [
    path('', ListCreateMembersView.as_view(), name='members_list'),
]
