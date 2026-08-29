import time
import hashlib
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.core.cache import cache

from leaderboard.models import CPProfile
from leaderboard.api.serializers import CPLeaderboardSerializer
from leaderboard.management.commands.sync_leaderboard import run_full_leaderboard_sync

COOLDOWN_SECONDS = 300  # 5 minutes refresh cooldown


class LeaderboardListView(generics.ListAPIView):
    """
    Returns ranked CP leaderboard for NIT Durgapur coders across Codeforces / CodeChef.
    Responses are cached in Redis with a 5-minute TTL.
    """
    serializer_class = CPLeaderboardSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        platform = request.query_params.get('platform', 'codeforces').lower()
        search = request.query_params.get('search', '').strip()
        batch = request.query_params.get('batch', None)
        show_inactive = (
            request.query_params.get('show_inactive', '') or 
            request.query_params.get('showInactive', '')
        ).lower() in ('true', '1')

        # Build Redis cache key
        cache_params = f"{platform}:{search}:{batch}:{show_inactive}"
        cache_hash = hashlib.md5(cache_params.encode('utf-8')).hexdigest()
        cache_key = f"leaderboard:list:{cache_hash}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        # Build QuerySet
        queryset = CPProfile.objects.filter(is_active=True)

        if platform == 'codechef':
            queryset = queryset.filter(codechef_handle__gt='', codechef_rating__gt=0)
            if not show_inactive:
                queryset = queryset.filter(codechef_is_active=True)
            queryset = queryset.order_by('-codechef_rating', '-codeforces_rating')
        else:
            # Default to codeforces
            platform = 'codeforces'
            queryset = queryset.filter(codeforces_handle__gt='', codeforces_rating__gt=0)
            if not show_inactive:
                queryset = queryset.filter(codeforces_is_active=True)
            queryset = queryset.order_by('-codeforces_rating', '-codechef_rating')

        if batch and batch.isdigit():
            queryset = queryset.filter(batch=int(batch))

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(username__icontains=search) |
                Q(codeforces_handle__icontains=search) |
                Q(codechef_handle__icontains=search)
            )

        serializer = self.get_serializer(queryset, many=True)
        serialized_results = serializer.data

        # Add relative ranking
        for index, item in enumerate(serialized_results, start=1):
            item['rank'] = index

        response_data = {
            'platform': platform,
            'count': len(serialized_results),
            'results': serialized_results,
        }

        # Cache in Redis for 5 minutes
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)


class LeaderboardCooldownView(APIView):
    """
    Returns current refresh cooldown status.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        last_refresh = cache.get("leaderboard:last_refresh_timestamp")
        current_time = time.time()

        if last_refresh:
            elapsed = current_time - float(last_refresh)
            if elapsed < COOLDOWN_SECONDS:
                remaining = int(COOLDOWN_SECONDS - elapsed)
                return Response({
                    "can_refresh": False,
                    "remaining_seconds": remaining,
                    "cooldown_total": COOLDOWN_SECONDS
                })

        return Response({
            "can_refresh": True,
            "remaining_seconds": 0,
            "cooldown_total": COOLDOWN_SECONDS
        })


class LeaderboardRefreshView(APIView):
    """
    Triggers live synchronization of standings from Codeforces Org #785 and CodeChef.
    Enforces a strict 5-minute Redis-based cooldown.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        last_refresh = cache.get("leaderboard:last_refresh_timestamp")
        current_time = time.time()

        if last_refresh:
            elapsed = current_time - float(last_refresh)
            if elapsed < COOLDOWN_SECONDS:
                remaining = int(COOLDOWN_SECONDS - elapsed)
                return Response({
                    "error": f"Please wait {remaining}s before refreshing again.",
                    "remaining_seconds": remaining,
                    "can_refresh": False
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Set new timestamp in Redis
        cache.set("leaderboard:last_refresh_timestamp", current_time, timeout=COOLDOWN_SECONDS)

        try:
            stats = run_full_leaderboard_sync()
            return Response({
                "message": "NIT Durgapur standings successfully refreshed from Codeforces & CodeChef!",
                "stats": stats,
                "cooldown_seconds": COOLDOWN_SECONDS
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Sync failed: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
