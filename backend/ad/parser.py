import os, json
from typing import List, Dict, TypedDict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class MyClass(TypedDict):
    name: str
    price: str
    description: str
    url: str

class PaginationParser:
    url = 'https://www.avito.ru/rossiya/avtomobili'
    max_page_count = 101
    data = []

    def __init__(self, max_page_count):
        if max_page_count:
            self.max_page_count = max_page_count + 1

    @property
    def clear_data(self) -> List[MyClass]:
        return json.loads(json.dumps(self.data, indent=4, sort_keys=True, ensure_ascii=False))

    def parse(self):
        service = Service(os.getenv("SELENIUM_ENGINE_PATH"))
        driver = webdriver.Chrome(service=service)
        results = []
        for i in range(1, self.max_page_count):
            driver.get(self.url + f"?p={i}")
            results = (driver.execute_script("""
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
            """))
        driver.quit()
        self.data = results


class AdParser:
    pass


if __name__ == "__main__":
    pagination_parser = PaginationParser(max_page_count=1)
    pagination_parser.parse()
    print(json.dumps(pagination_parser.clear_data, indent=4, sort_keys=True, ensure_ascii=False))


