from datetime import datetime, timedelta

import pytz

CACHE_KEY = 'contest_notifications_data'
IST = pytz.timezone('Asia/Kolkata')


def get_last_refresh_boundary(now=None):
    """Return the most recent 12:01 AM IST boundary before *now*."""
    if now is None:
        now = datetime.now(IST)
    elif now.tzinfo is None:
        now = IST.localize(now)
    else:
        now = now.astimezone(IST)

    boundary = now.replace(hour=0, minute=1, second=0, microsecond=0)
    if now < boundary:
        boundary -= timedelta(days=1)
    return boundary


def is_cache_fresh(cached_at):
    if not cached_at:
        return False

    if isinstance(cached_at, str):
        cached_at = datetime.fromisoformat(cached_at.replace('Z', '+00:00'))

    if cached_at.tzinfo is None:
        cached_at = IST.localize(cached_at)
    else:
        cached_at = cached_at.astimezone(IST)

    return cached_at >= get_last_refresh_boundary()
