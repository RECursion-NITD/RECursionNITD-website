from rest_framework import serializers
from leaderboard.models import CPProfile


class CPLeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPProfile
        fields = [
            'id',
            'name',
            'username',
            'college',
            'batch',
            'dept',
            'codeforces_handle',
            'codeforces_rating',
            'codeforces_max_rating',
            'codeforces_rank',
            'codeforces_contests',
            'codeforces_solved',
            'codeforces_is_active',
            'codechef_handle',
            'codechef_rating',
            'codechef_stars',
            'codechef_global_rank',
            'codechef_contests',
            'codechef_is_active',
            'avatar_url',
            'last_synced',
        ]
