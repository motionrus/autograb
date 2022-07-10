import django_rq
from rq import Worker

from ad.models import Ad
from ad.parser import PaginationParser
from redis import StrictRedis


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class SingleTonJob:
    job = ""
    percentage = 0

    def get_job(self):
        if not self.job:
            self.job = django_rq.enqueue(work_ads)
        return self.job

    def get_connection(self):
        return self.get_job().get_connection('default')


def save(clear_data, percentage):
    for data in clear_data:
        SingleTonJob().percentage = percentage

        ad, created = Ad.objects.update_or_create(url=data['url'], defaults=data)
        if not created:
            ad.save()


def work_ads(*args, **kwargs):
    pagination_parser = PaginationParser(max_page_count=100)
    pagination_parser.parse(callback=save)
