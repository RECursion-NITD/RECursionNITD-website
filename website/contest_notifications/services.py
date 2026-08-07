from datetime import datetime, timezone

import pytz
import requests
from django.conf import settings
from django.core.cache import cache

from .cache_utils import CACHE_KEY, IST, get_last_refresh_boundary, is_cache_fresh

CLIST_BASE_URL = 'https://clist.by/api/v4/json/contest/'
PLATFORM_RESOURCES = {
    'codeforces': 'codeforces.com',
    'codechef': 'codechef.com',
    'atcoder': 'atcoder.jp',
}
RESOURCE_ID_PLATFORMS = {
    1: 'codeforces',
    2: 'codechef',
    93: 'atcoder',
}
RESOURCE_LABELS = {
    'codeforces.com': 'Codeforces',
    'codechef.com': 'CodeChef',
    'atcoder.jp': 'AtCoder',
    'codeforces': 'Codeforces',
    'codechef': 'CodeChef',
    'atcoder': 'AtCoder',
}


def _ordinal(day):
    if 11 <= day % 100 <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return f'{day}{suffix}'


def _format_start_time(dt):
    dt = dt.astimezone(IST)
    hour = dt.hour
    minute = dt.minute
    period = 'am' if hour < 12 else 'pm'
    display_hour = hour % 12 or 12
    return (
        f'{_ordinal(dt.day)} {dt.strftime("%B")}, {dt.year} '
        f'at {display_hour:02d}:{minute:02d} {period} IST'
    )


def _format_duration(seconds):
    if not seconds:
        return 'unknown duration'

    total_minutes = int(seconds) // 60
    hours, minutes = divmod(total_minutes, 60)

    if hours and minutes:
        hour_label = 'hour' if hours == 1 else 'hours'
        minute_label = 'minute' if minutes == 1 else 'minutes'
        return f'{hours} {hour_label} {minutes} {minute_label}'

    if hours:
        return f'{hours} hour{"s" if hours != 1 else ""}'

    return f'{minutes} minute{"s" if minutes != 1 else ""}'


def _build_notification_text(name, start_dt, duration_seconds, url):
    start_text = _format_start_time(start_dt)
    duration_text = _format_duration(duration_seconds)
    return (
        f'{name} will start on {start_text}.\n'
        f'Contest duration is {duration_text}.\n\n'
        f'Contest link: {url}\n'
        f'Happy Coding! 😀'
    )


def _parse_clist_datetime(value):
    if not value:
        return None

    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        # Clist returns UTC timestamps without a timezone suffix.
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(IST)


def _should_include_contest(platform, name):
    normalized_name = (name or '').lower()

    if platform == 'codeforces':
        return True
    if platform == 'codechef':
        return 'starter' in normalized_name
    if platform == 'atcoder':
        return 'beginner' in normalized_name

    return True


def _normalize_contest(item):
    resource = item.get('resource', '')
    resource_id = item.get('resource_id')

    platform = RESOURCE_ID_PLATFORMS.get(resource_id)
    if not platform:
        platform = next(
            (key for key, host in PLATFORM_RESOURCES.items() if host == resource),
            resource.replace('.com', '').replace('.jp', ''),
        )

    start_dt = _parse_clist_datetime(item.get('start'))
    end_dt = _parse_clist_datetime(item.get('end'))

    duration_seconds = item.get('duration')
    if not duration_seconds and start_dt and end_dt:
        duration_seconds = int((end_dt - start_dt).total_seconds())

    name = item.get('event') or item.get('name') or 'Upcoming Contest'
    url = item.get('href') or item.get('url') or ''

    return {
        'platform': platform,
        'platform_label': RESOURCE_LABELS.get(platform, RESOURCE_LABELS.get(resource, platform.title())),
        'name': name,
        'start_time': start_dt.isoformat() if start_dt else None,
        'start_time_ist': _format_start_time(start_dt) if start_dt else None,
        'duration_seconds': duration_seconds,
        'duration_text': _format_duration(duration_seconds),
        'url': url,
        'notification_text': _build_notification_text(name, start_dt, duration_seconds, url)
        if start_dt and url
        else None,
    }


def fetch_contests_from_clist():
    username = settings.CLIST_USERNAME
    api_key = settings.CLIST_API_KEY

    if not username or not api_key:
        raise ValueError('CLIST_USERNAME and CLIST_API_KEY must be configured.')

    now = datetime.now(IST)
    params = {
        'username': username,
        'api_key': api_key,
        'resource_id__in': settings.CLIST_RESOURCE_IDS,
        'upcoming': 'true',
        'order_by': 'start',
        'limit': 100,
    }

    response = requests.get(
        CLIST_BASE_URL,
        params=params,
        timeout=30,
        headers={'User-Agent': 'RecursionContestBot/1.0'},
    )
    response.raise_for_status()
    payload = response.json()

    contests = []
    for item in payload.get('objects', []):
        normalized = _normalize_contest(item)
        if (
            normalized['notification_text']
            and _should_include_contest(normalized['platform'], normalized['name'])
        ):
            contests.append(normalized)

    contests.sort(key=lambda contest: contest['start_time'] or '')
    return {
        'cached_at': now.isoformat(),
        'refresh_boundary': get_last_refresh_boundary(now).isoformat(),
        'contests': contests,
    }


def refresh_contest_cache(force=False):
    cached_payload = cache.get(CACHE_KEY)

    if not force and cached_payload and is_cache_fresh(cached_payload.get('cached_at')):
        return cached_payload

    payload = fetch_contests_from_clist()
    cache.set(CACHE_KEY, payload, timeout=60 * 60 * 26)
    return payload


def get_cached_contests():
    cached_payload = cache.get(CACHE_KEY)
    if cached_payload and is_cache_fresh(cached_payload.get('cached_at')):
        return cached_payload

    return refresh_contest_cache(force=True)
