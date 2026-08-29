import logging
from django.core.management.base import BaseCommand
from django.core.cache import cache
from leaderboard.models import CPProfile
from leaderboard.services.codeforces_sync import (
    fetch_codeforces_org_members,
    fetch_codeforces_batch,
    extract_cf_handle
)
from leaderboard.services.codechef_sync import (
    fetch_codechef_institution_members,
    extract_cc_handle
)
from user_profile.models import Profile

logger = logging.getLogger(__name__)


def run_full_leaderboard_sync():
    """
    Performs full synchronization of NIT Durgapur CP standings directly from:
    1. Codeforces Org #785 (NIT Durgapur)
    2. CodeChef Institution ratings (National Institute of Technology, Durgapur)
    3. Registered users with handles
    Invalidates Redis cache upon completion.
    """
    stats = {
        "cf_scraped": 0,
        "cc_scraped": 0,
        "users_synced": 0,
        "total_profiles": 0
    }

    # 1. Scrape Codeforces Organization #785
    cf_org_members = fetch_codeforces_org_members(org_id="785")
    if cf_org_members:
        cf_batch_info = fetch_codeforces_batch(list(cf_org_members.keys()))
        for h_lower, org_data in cf_org_members.items():
            cf_info = cf_batch_info.get(h_lower, {})
            name = cf_info.get('name') or org_data['handle']
            rating = cf_info.get('rating') or org_data.get('rating', 0)
            max_rating = cf_info.get('max_rating', rating)
            rank = cf_info.get('rank', 'Unrated')
            avatar = cf_info.get('avatar')
            contests = org_data.get('contests', 0)

            cf_active = org_data.get('is_active', True)

            cp, _ = CPProfile.objects.update_or_create(
                codeforces_handle__iexact=org_data['handle'],
                defaults={
                    'name': name,
                    'codeforces_handle': org_data['handle'],
                    'codeforces_rating': rating,
                    'codeforces_max_rating': max_rating,
                    'codeforces_rank': rank,
                    'codeforces_contests': contests,
                    'codeforces_is_active': cf_active,
                    'avatar_url': avatar,
                    'college': 'National Institute of Technology, Durgapur'
                }
            )
            stats["cf_scraped"] += 1

    # 2. Scrape CodeChef Institution (NIT Durgapur)
    cc_members = fetch_codechef_institution_members(max_pages=10)
    for h_lower, cc_data in cc_members.items():
        handle = cc_data['handle']
        name = cc_data.get('name') or handle
        rating = cc_data.get('rating', 0)
        stars = cc_data.get('stars', '')
        global_rank = cc_data.get('global_rank')
        cc_active = cc_data.get('is_active', True)

        # Try to find existing by CodeChef handle or name
        cp = CPProfile.objects.filter(codechef_handle__iexact=handle).first()
        if cp:
            if not cp.name or cp.name == cp.codeforces_handle:
                cp.name = name
            cp.codechef_rating = rating
            cp.codechef_stars = stars
            cp.codechef_global_rank = global_rank
            cp.codechef_is_active = cc_active
            cp.save()
        else:
            CPProfile.objects.create(
                name=name,
                codechef_handle=handle,
                codechef_rating=rating,
                codechef_stars=stars,
                codechef_global_rank=global_rank,
                codechef_is_active=cc_active,
                college='National Institute of Technology, Durgapur'
            )
        stats["cc_scraped"] += 1

    # 3. Sync Registered Users with Handles
    registered = Profile.objects.filter(email_confirmed=True)
    for p in registered:
        cf_h = extract_cf_handle(p.url_Codeforces)
        cc_h = extract_cc_handle(p.url_CodeChef)
        if cf_h or cc_h:
            cp = None
            if cf_h:
                cp = CPProfile.objects.filter(codeforces_handle__iexact=cf_h).first()
            if not cp and cc_h:
                cp = CPProfile.objects.filter(codechef_handle__iexact=cc_h).first()

            if cp:
                cp.user = p.user
                if p.name:
                    cp.name = p.name
                if p.dept:
                    cp.dept = p.dept
                if cf_h and not cp.codeforces_handle:
                    cp.codeforces_handle = cf_h
                if cc_h and not cp.codechef_handle:
                    cp.codechef_handle = cc_h
                cp.save()
            else:
                CPProfile.objects.create(
                    user=p.user,
                    name=p.name or p.user.username,
                    username=p.user.username,
                    dept=p.dept or '',
                    codeforces_handle=cf_h,
                    codechef_handle=cc_h,
                    college=p.college or 'National Institute of Technology, Durgapur'
                )
            stats["users_synced"] += 1

    stats["total_profiles"] = CPProfile.objects.count()

    # 4. Invalidate all leaderboard Redis cache entries
    try:
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern("leaderboard:*")
        else:
            cache.clear()
    except Exception as e:
        logger.warning(f"Failed to clear Redis cache: {e}")

    return stats


class Command(BaseCommand):
    help = "Synchronizes Codeforces Org 785 and CodeChef NIT Durgapur live standings"

    def handle(self, *args, **options):
        self.stdout.write("Starting real NIT Durgapur CP Leaderboard sync...")
        stats = run_full_leaderboard_sync()
        self.stdout.write(
            f"Successfully synced: {stats['cf_scraped']} CF members, "
            f"{stats['cc_scraped']} CC members, {stats['users_synced']} registered users. "
            f"Total profiles: {stats['total_profiles']}."
        )
