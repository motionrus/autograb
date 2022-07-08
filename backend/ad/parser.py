import os, json
import time
from typing import List, Dict, TypedDict

from selenium import webdriver


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

    def __init__(self, max_page_count=0):
        if max_page_count:
            self.max_page_count = max_page_count + 1
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )

    @property
    def clear_data(self) -> List[MyClass]:
        return json.loads(json.dumps(self.data, indent=4, sort_keys=True, ensure_ascii=False))

    def parse(self, callback=lambda x: x):
        results = []
        for i in range(1, self.max_page_count):
            time.sleep(1)
            callback(self.get_ads(self.url + f"?p={i}"))
        self.driver.quit()
        self.data = results

    def get_ads(self, url):
        print(url)
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


class AdParser(PaginationParser):
    def get_best_price(self, url):
        self.driver.get(url)
        return self.driver.execute_script("""
            const result = document.querySelector('h4[class*=styles-heading]')?.nextElementSibling.firstChild.textContent
            return result ? result.replace(/\xA0/g,' ') : ""
        """)


if __name__ == "__main__":
    pagination_parser = PaginationParser(max_page_count=1)
    pagination_parser.parse()
    print(json.dumps(pagination_parser.clear_data, indent=4, sort_keys=True, ensure_ascii=False))
