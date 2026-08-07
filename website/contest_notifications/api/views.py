from rest_framework.response import Response
from rest_framework.views import APIView

from contest_notifications.services import get_cached_contests, refresh_contest_cache


class ContestNotificationsView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        platform = request.query_params.get('platform')

        try:
            payload = get_cached_contests()
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=503)
        except Exception as exc:
            return Response(
                {'detail': f'Failed to fetch contests: {exc}'},
                status=502,
            )

        contests = payload.get('contests', [])
        if platform:
            contests = [
                contest for contest in contests
                if contest.get('platform') == platform.lower()
            ]

        return Response({
            'cached_at': payload.get('cached_at'),
            'refresh_boundary': payload.get('refresh_boundary'),
            'contests': contests,
        })


class ContestNotificationsRefreshView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            payload = refresh_contest_cache(force=True)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=503)
        except Exception as exc:
            return Response(
                {'detail': f'Failed to refresh contests: {exc}'},
                status=502,
            )

        return Response({
            'cached_at': payload.get('cached_at'),
            'refresh_boundary': payload.get('refresh_boundary'),
            'contest_count': len(payload.get('contests', [])),
        })
