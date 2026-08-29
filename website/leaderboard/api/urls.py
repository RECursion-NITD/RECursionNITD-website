from django.urls import path
from leaderboard.api.views import (
    LeaderboardListView,
    LeaderboardRefreshView,
    LeaderboardCooldownView
)

app_name = 'leaderboard_api'

urlpatterns = [
    path('', LeaderboardListView.as_view(), name='leaderboard_list'),
    path('refresh/', LeaderboardRefreshView.as_view(), name='leaderboard_refresh'),
    path('cooldown/', LeaderboardCooldownView.as_view(), name='leaderboard_cooldown'),
]
