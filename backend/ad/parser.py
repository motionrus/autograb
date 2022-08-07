import datetime
import os, json
import time
from typing import List, Dict, TypedDict
from rq import Queue
from redis import Redis
import django_rq
from selenium import webdriver

from ad.models import Ad


class MyClass(TypedDict):
    name: str
    price: str
    description: str
    url: str


class PaginationParser:
    count_tries = 3

    def __init__(self, url, script):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(
            command_executor=os.getenv("SELENIUM_URL"),
            options=options
        )
        self.url = url
        self.script = script

    def parse(self):
        self.driver.get(self.url)
        count = self.count_tries
        while count:
            result = self.driver.execute_script(self.script)
            if not result:
                self.driver.refresh()
                time.sleep(2)
                count -= 1
            else:
                return result

    def quit(self):
        time.sleep(1)
        self.driver.quit()


def save(cars):
    for car in cars:
        ad, created = Ad.objects.update_or_create(url=car['url'], defaults=car)
        if not created:
            ad.save()


def clear_data(data) -> List[MyClass]:
    return json.loads(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))


def parse_pages(page):
    script = """
        return [...document.querySelector('[data-marker=catalog-serp]')
            ?.querySelectorAll('[data-marker=item]')]?.map(marker => {
                const body = marker.querySelector('div[class*=body]')
                return {
                    name: body.querySelector('div[class*=titleStep]')?.textContent,
                    price: body.querySelector('div[class*=priceStep]')?.textContent.replace(/\xA0/g,' '),
                    description: body.querySelector('div[class*=descriptionStep]')?.textContent || '',
                    url: body.querySelector('a').href
                }
            })
    """
    url = f'https://www.avito.ru/rossiya/avtomobili?p={page}'
    parser = PaginationParser(url, script)
    cars = clear_data(parser.parse())
    save(cars)

    q = django_rq.get_queue('default')
    urls = [x.args[0] for x in q.get_jobs()]

    for car in cars:
        ads = Ad.objects.filter(url__exact=car["url"]).first()
        need_updates = ads and ads.need_updates or False
        if need_updates and car["url"] not in urls:
            django_rq.enqueue(parse_cars, car["url"])

    parser.quit()


def parse_cars(url):
    ad = Ad.objects.filter(url__exact=url).first()
    script = """
        const result = document.querySelector('h4[class*=styles-heading]')?.nextElementSibling.firstChild.textContent
        return result ? result.replace(/\xA0/g,' ') : ""
    """
    parser = PaginationParser(ad.url, script)
    ad.rating = parser.parse()
    ad.save()
    parser.quit()


if __name__ == "__main__":
    pagination_parser = PaginationParser(max_page_count=1)
    pagination_parser.run()
    print(json.dumps(pagination_parser.clear_data, indent=4, sort_keys=True, ensure_ascii=False))
