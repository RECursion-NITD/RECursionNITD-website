from django.urls import path

from .views import ContestNotificationsRefreshView, ContestNotificationsView

app_name = 'contest_notifications_api'

urlpatterns = [
    path('', ContestNotificationsView.as_view(), name='contest_notifications'),
    path('refresh/', ContestNotificationsRefreshView.as_view(), name='contest_notifications_refresh'),
]
