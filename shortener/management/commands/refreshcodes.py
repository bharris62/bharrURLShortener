from django.core.management.base import BaseCommand, CommandError
from shortener.models import BharrURL

class Command(BaseCommand):
    help = 'refreshes all the shortcodes.'

    def add_arguments(self, parser):
        parser.add_argument('items', type=int)

    def handle(self, *args, **options):
        return BharrURL.objects.refresh_shortcodes(items=options['items'])