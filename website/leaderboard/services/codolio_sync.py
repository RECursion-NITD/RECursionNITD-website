import re
import logging
import requests

logger = logging.getLogger(__name__)


def extract_codolio_handle(url_or_handle):
    """
    Extracts raw handle from Codolio profile URLs or plain text.
    e.g. 'https://codolio.com/profile/username' -> 'username'
    """
    if not url_or_handle:
        return ''
    raw = str(url_or_handle).strip().rstrip('/')
    if 'codolio.com/profile/' in raw:
        return raw.split('codolio.com/profile/')[-1].split('/')[0].split('?')[0].strip()
    match = re.search(r'([a-zA-Z0-9_.-]+)$', raw)
    return match.group(1) if match else raw


def fetch_codolio_college_roster(college_query="National Institute of Technology Durgapur"):
    """
    Optional helper to fetch or query public college leaderboard data from Codolio if accessible.
    """
    url = f"https://api.codolio.com/leaderboard?college={requests.utils.quote(college_query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            return res.json().get('data', [])
    except Exception as e:
        logger.debug(f"Codolio API direct fetch skipped or unavailable: {e}")
    return []
