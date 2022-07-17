import os, json
import time
from typing import List, Dict, TypedDict

import django_rq
from selenium import webdriver

from ad.models import Ad


class MyClass(TypedDict):
    name: str
    price: str
    description: str
    url: str


class PaginationParser:
    url = 'https://www.avito.ru/rossiya/avtomobili'
    max_page_count = 101
    data = []
    count_tries = 3

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(
            command_executor=os.getenv("SELENIUM_URL"),
            options=options
        )

    @property
    def clear_data(self) -> List[MyClass]:
        return json.loads(json.dumps(self.data, indent=4, sort_keys=True, ensure_ascii=False))

    def save(self):
        for data in self.clear_data:
            ad, created = Ad.objects.update_or_create(url=data['url'], defaults=data)
            if not created:
                ad.save()

    def parse(self, i):
        self.data = self.get_ads(self.url + f"?p={i}")
        self.driver.quit()
        self.save()

    def get_ads(self, url):
        self.driver.get(url)
        return self.driver.execute_script("""
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
        """)


def parse(count):
    parser = PaginationParser()
    parser.parse(count)
    for i in parser.clear_data:
        django_rq.enqueue(parse_ads, i["url"])


class AdParser(PaginationParser):
    def get_best_price(self, url):
        self.driver.get(url)
        return self.driver.execute_script("""
            const result = document.querySelector('h4[class*=styles-heading]')?.nextElementSibling.firstChild.textContent
            return result ? result.replace(/\xA0/g,' ') : ""
        """)


def parse_ads(url):
    AdParser().parse(url)


if __name__ == "__main__":
    pagination_parser = PaginationParser(max_page_count=1)
    pagination_parser.parse()
    print(json.dumps(pagination_parser.clear_data, indent=4, sort_keys=True, ensure_ascii=False))
