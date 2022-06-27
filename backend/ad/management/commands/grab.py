from django.core.management.base import BaseCommand, CommandError

from ad.models import Ad
from ad.parser import PaginationParser


class Command(BaseCommand):
    help = 'Grab Avito'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pagination_parser = PaginationParser(max_page_count=1)
        pagination_parser.parse()

        for data in pagination_parser.clear_data:
            ad, created = Ad.objects.get_or_create(url=data['url'], defaults=data)
            if not created:
                ad.name = data['name']
                ad.description = data['description']
                ad.price = data['price']
                ad.save()

