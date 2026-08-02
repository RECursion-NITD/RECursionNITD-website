from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import mimetypes
import logging
import requests
from disposable_email_domains import blocklist
from django.core.cache import cache

logger = logging.getLogger(__name__)

DEBOUNCE_API_URL = 'https://disposable.debounce.io/'
DEBOUNCE_TIMEOUT = 2  # seconds
CACHE_TTL = 60 * 60 * 24  # cache domain results for 24 hours


VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]

def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    return any([url.endswith(e) for e in extension_list])


VALID_IMAGE_MIMETYPES = [
    "image"
]

def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def is_disposable_email(email: str) -> bool:
    """
    Returns True if the email's domain is a known disposable/temp-mail domain.
    Checks local blocklist first (instant, free), falls back to DeBounce API
    for domains not yet in the local list.
    """
    if not email or '@' not in email:
        return False

    email = email.strip().lower()
    domain = email.split('@')[-1]

    # 1. Fast local check — no network call
    if domain in blocklist:
        logger.info(f"Blocked disposable email via local blocklist: {domain}")
        return True

    # 2. Check cache before hitting the API (avoid re-checking same domain repeatedly)
    cache_key = f"disposable_check:{domain}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    # 3. Live API check for domains not in local list yet
    try:
        response = requests.get(
            DEBOUNCE_API_URL,
            params={'email': email},
            timeout=DEBOUNCE_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        is_disposable = str(data.get('disposable', 'false')).lower() == 'true'

        cache.set(cache_key, is_disposable, CACHE_TTL)

        if is_disposable:
            logger.info(f"Blocked disposable email via DeBounce API: {domain}")

        return is_disposable

    except (requests.RequestException, ValueError) as e:
        # Fail open — never block real signups because a 3rd party API is down/slow
        logger.warning(f"DeBounce API check failed for {domain}: {e}")
        return False