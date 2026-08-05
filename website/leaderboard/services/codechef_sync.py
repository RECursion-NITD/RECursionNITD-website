import re
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract_cc_handle(url_or_handle):
    """
    Extracts raw handle from CodeChef URLs or plain text.
    e.g. 'https://www.codechef.com/users/gennady' -> 'gennady'
    """
    if not url_or_handle:
        return ''
    raw = str(url_or_handle).strip().rstrip('/')
    if 'codechef.com/users/' in raw:
        return raw.split('codechef.com/users/')[-1].split('/')[0].split('?')[0].strip()
    match = re.search(r'([a-zA-Z0-9_.-]+)$', raw)
    return match.group(1) if match else raw


def calculate_cc_stars(rating):
    if not rating or rating <= 0:
        return ''
    if rating >= 2500:
        return '7★'
    elif rating >= 2200:
        return '6★'
    elif rating >= 2000:
        return '5★'
    elif rating >= 1800:
        return '4★'
    elif rating >= 1600:
        return '3★'
    elif rating >= 1400:
        return '2★'
    return '1★'


def fetch_codechef_institution_members(max_pages=5):
    """
    Scrapes the official CodeChef ratings for National Institute of Technology, Durgapur.
    Uses CodeChef's rating API with session cookies and CSRF token extraction.
    Returns a dict mapping handle_lower -> { 'handle', 'name', 'rating', 'stars', 'global_rank' }
    """
    s = requests.Session()
    page_url = (
        "https://www.codechef.com/ratings/all?"
        "filterBy=Country%3DIndia%3BInstitution%3DNational%20Institute%20of%20Technology%2C%20Durgapur%20"
        "&itemsPerPage=50&order=asc&page=1&sortBy=global_rank"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    members = {}
    try:
        r = s.get(page_url, headers=headers, timeout=15)
        m = re.search(r'window\.csrfToken\s*=\s*["\']([^"\']+)["\']', r.text)
        csrf_token = m.group(1) if m else None

        for page in range(1, max_pages + 1):
            api_url = (
                f"https://www.codechef.com/api/ratings/all?"
                f"filterBy=Country%3DIndia%3BInstitution%3DNational%20Institute%20of%20Technology%2C%20Durgapur%20"
                f"&itemsPerPage=50&order=asc&page={page}&sortBy=global_rank"
            )
            api_headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "x-csrf-token": csrf_token or "",
                "x-requested-with": "XMLHttpRequest",
                "Referer": page_url
            }

            resp = s.get(api_url, headers=api_headers, timeout=15)
            if resp.status_code != 200:
                break

            data = resp.json()
            items = data.get('list', [])
            if not items:
                break

            for item in items:
                username = item.get('username')
                if not username:
                    continue
                clean_h = extract_cc_handle(username)
                if not clean_h:
                    continue

                raw_rating = item.get('rating')
                try:
                    rating = int(raw_rating) if raw_rating else 0
                except (ValueError, TypeError):
                    rating = 0

                raw_gr = item.get('global_rank')
                try:
                    global_rank = int(raw_gr) if raw_gr else None
                except (ValueError, TypeError):
                    global_rank = None

                stars = item.get('stars') or calculate_cc_stars(rating)
                name = item.get('name', '').strip()
                is_active = (not item.get('is_provisional_rating', False)) and (rating > 0)

                members[clean_h.lower()] = {
                    'handle': clean_h,
                    'name': name,
                    'rating': rating,
                    'stars': stars,
                    'global_rank': global_rank,
                    'is_active': is_active,
                }

            # Stop if we fetched all available pages
            available_pages = data.get('availablePages', 1)
            if page >= available_pages:
                break

    except Exception as e:
        logger.error(f"Failed to scrape CodeChef institution members: {e}")

    return members


def fetch_codechef_profile(handle):
    """
    Fetches individual CodeChef profile rating and star rank as a fallback.
    """
    clean_handle = extract_cc_handle(handle)
    if not clean_handle:
        return None

    url = f"https://www.codechef.com/users/{clean_handle}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')

        # Rating Number
        rating_div = soup.find('div', class_='rating-number')
        rating = 0
        if rating_div:
            rating_match = re.search(r'\d+', rating_div.text)
            if rating_match:
                rating = int(rating_match.group(0))

        stars = calculate_cc_stars(rating)

        # Global Rank
        global_rank = None
        rank_links = soup.find_all('a', href=re.compile(r'/ratings/all'))
        for link in rank_links:
            parent = link.find_parent('li') or link.parent
            if parent and 'Global Rank' in parent.text:
                rank_match = re.search(r'\d+', link.text.replace(',', ''))
                if rank_match:
                    global_rank = int(rank_match.group(0))
                    break

        return {
            'handle': clean_handle,
            'rating': rating,
            'stars': stars,
            'global_rank': global_rank,
        }
    except Exception as e:
        logger.error(f"Error scraping CodeChef for {clean_handle}: {e}")
        return None
