from django.core.management.base import BaseCommand, CommandError

from ad.models import Ad
from ad.parser import PaginationParser


class Command(BaseCommand):
    help = 'Grab Avito'

    def add_arguments(self, parser):
        pass

    @staticmethod
    def save(clear_data):
        for data in clear_data:
            ad, created = Ad.objects.update_or_create(url=data['url'], defaults=data)
            if not created:
                ad.save()

    def handle(self, *args, **options):

        pagination_parser = PaginationParser(max_page_count=100)
        pagination_parser.parse(callback=self.save)
