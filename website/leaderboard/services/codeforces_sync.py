import re
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Valid Codeforces handle: 3-24 chars, letters, digits, underscores, periods, hyphens
HANDLE_REGEX = re.compile(r'^[a-zA-Z0-9_.-]{3,24}$')
INVALID_KEYWORDS = {'something.com', 'test.com', 'editprofile', 'www.codeforces.com', 'codeforces.com', 'http', 'https'}


def extract_cf_handle(url_or_handle):
    """
    Extracts raw handle from various URL formats or plain text.
    e.g. 'https://codeforces.com/profile/tourist' -> 'tourist'
    """
    if not url_or_handle:
        return ''
    raw = str(url_or_handle).strip().rstrip('/')
    if 'codeforces.com/profile/' in raw:
        raw = raw.split('codeforces.com/profile/')[-1].split('/')[0].split('?')[0].strip()
    elif 'codeforces.com/' in raw:
        raw = raw.split('codeforces.com/')[-1].split('/')[0].split('?')[0].strip()

    match = re.search(r'([a-zA-Z0-9_.-]+)$', raw)
    handle = match.group(1) if match else raw
    if handle.lower() in INVALID_KEYWORDS or handle.endswith('.com'):
        return ''
    if not HANDLE_REGEX.match(handle):
        return ''
    return handle


def fetch_codeforces_org_members(org_id="785"):
    """
    Since scraping the org page is blocked by Cloudflare on AWS, 
    we fetch all rated users globally via API and filter for NIT Durgapur.
    """
    url_all = "https://codeforces.com/api/user.ratedList?activeOnly=false"
    members = {}
    try:
        res = requests.get(url_all, timeout=30)
        if res.status_code == 200:
            data = res.json()
            if data.get('status') == 'OK':
                for u in data.get('result', []):
                    org = u.get('organization', '').lower()
                    org = org.replace(',', ' ')
                    if 'nit durgapur' in org or ('national institute of technology' in org and 'durgapur' in org):
                        handle = u.get('handle')
                        clean_h = extract_cf_handle(handle)
                        if clean_h:
                            members[clean_h.lower()] = {
                                'handle': clean_h,
                                'contests': 0,
                                'rating': u.get('rating', 0),
                                'is_active': True
                            }
    except Exception as e:
        logger.error(f"Failed to fetch CF org members via API: {e}")
    return members


def _fetch_single_cf(handle, headers):
    try:
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get('status') == 'OK' and data.get('result'):
                user_info = data['result'][0]
                first = user_info.get('firstName', '').strip()
                last = user_info.get('lastName', '').strip()
                full_name = f"{first} {last}".strip()
                return {
                    'handle': user_info.get('handle'),
                    'name': full_name,
                    'rating': user_info.get('rating', 0),
                    'max_rating': user_info.get('maxRating', 0),
                    'rank': user_info.get('rank', 'Unrated').title(),
                    'avatar': user_info.get('titlePhoto') or user_info.get('avatar'),
                }
    except Exception:
        pass
    return None


def fetch_codeforces_batch(handles, chunk_size=40):
    """
    Fetches Codeforces user info in batches using the official Codeforces API.
    If a batch fails (due to 1 invalid handle), falls back to individual lookups.
    """
    cleaned_handles = list(dict.fromkeys(filter(None, [extract_cf_handle(h) for h in handles])))
    if not cleaned_handles:
        return {}

    results = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (RECursion-NITD CP Leaderboard Tracker; https://recursionnitd.in)'
    }

    for i in range(0, len(cleaned_handles), chunk_size):
        chunk = cleaned_handles[i:i + chunk_size]
        query_str = ';'.join(chunk)
        url = f"https://codeforces.com/api/user.info?handles={query_str}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get('status') == 'OK':
                    for user_info in data.get('result', []):
                        handle_key = user_info.get('handle', '').lower()
                        first = user_info.get('firstName', '').strip()
                        last = user_info.get('lastName', '').strip()
                        full_name = f"{first} {last}".strip()
                        results[handle_key] = {
                            'handle': user_info.get('handle'),
                            'name': full_name,
                            'rating': user_info.get('rating', 0),
                            'max_rating': user_info.get('maxRating', 0),
                            'rank': user_info.get('rank', 'Unrated').title(),
                            'avatar': user_info.get('titlePhoto') or user_info.get('avatar'),
                        }
            else:
                for h in chunk:
                    single_res = _fetch_single_cf(h, headers)
                    if single_res:
                        results[single_res['handle'].lower()] = single_res
        except Exception as e:
            logger.error(f"Error fetching Codeforces batch: {e}")
            for h in chunk:
                single_res = _fetch_single_cf(h, headers)
                if single_res:
                    results[single_res['handle'].lower()] = single_res

    return results
