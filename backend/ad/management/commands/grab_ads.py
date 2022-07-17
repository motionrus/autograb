from django.core.management.base import BaseCommand, CommandError

from ad.models import Ad
from ad.parser import PaginationParser, AdParser


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
        ad_parser = AdParser()
        ads = Ad.objects.all()
        count = 0
        ads_count = ads.count()
        for ad in ads:
            count += 1
            print(f"{int(count / ads_count * 100)}/100% ad.url")
            ad.rating = ad_parser.get_best_price(ad.url)
            ad.save()
