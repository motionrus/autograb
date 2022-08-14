import datetime
import os, json
import time
import random
from typing import List, TypedDict

import django_rq

from ad.driver import driver
from ad.models import Ad


class MyClass(TypedDict):
    name: str
    price: str
    description: str
    url: str


class PaginationParser:
    count_tries = 2

    def __init__(self, url, script):
        self.driver = driver
        self.url = url
        self.script = script

    def parse(self):
        self.driver.get(self.url)
        count = self.count_tries
        while count:
            time.sleep(random.randint(2, 5))
            result = self.driver.execute_script(self.script)
            if not result:
                self.driver.refresh()
                count -= 1
            else:
                return result

    def quit(self):
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
                const price = Number((body.querySelector('div[class*=priceStep]')?.textContent.replace(/\xA0/g, '').replace(/ /gu, '').match(/\d+/)))
                return {
                    name: body.querySelector('div[class*=titleStep]')?.textContent,
                    price: price ? price : undefined,
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


def parse_cars(url):
    ad = Ad.objects.filter(url__exact=url).first()
    script = """
        getPrice = () => {
            toNumber = (node) => node.innerText.split('—').map(i => i.replace(/[^\d]/gu, '')).filter(i => i !== '').map(i => Number(i))
            getMediumPrice = (arrNumbers) => arrNumbers.length ? arrNumbers.reduce((previousValue, currentValue) => previousValue + currentValue) / arrNumbers.length : 0
            nodes = [...document.querySelectorAll('span')].filter(i => i.innerText === 'Подробнее об оценке')[0]?.parentNode?.parentNode?.parentNode?.parentNode
            textNodes = nodes ? [...nodes?.querySelectorAll('span')].filter(i => i.innerText) : []
            arrPrice = textNodes.map(t => toNumber(t)).filter(i => Boolean(i.length))
            if (arrPrice.length && arrPrice.length < 6 ) {
                medium = getMediumPrice(arrPrice.filter(arr => arr.length === 2)[0] || [])
                return Math.round(medium - arrPrice[0])	
            }
        }
        return getPrice()
    """
    parser = PaginationParser(ad.url, script)
    ad.rating = parser.parse()
    ad.save()
