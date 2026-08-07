from django.core.management.base import BaseCommand

from contest_notifications.services import refresh_contest_cache


class Command(BaseCommand):
    help = 'Fetch upcoming contests from Clist and refresh the server cache.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Refresh even if the current cache is still valid.',
        )

    def handle(self, *args, **options):
        payload = refresh_contest_cache(force=options['force'])
        contest_count = len(payload.get('contests', []))
        self.stdout.write(
            self.style.SUCCESS(
                f'Contest cache refreshed at {payload.get("cached_at")} '
                f'with {contest_count} contests.'
            )
        )
