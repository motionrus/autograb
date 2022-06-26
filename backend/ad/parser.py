import os

from selenium import webdriver


class PaginationParser:
    url = 'https://www.avito.ru/rossiya/avtomobili'
    max_page_count = 101

    def __init__(self, max_page_count):
        if max_page_count:
            self.max_page_count = max_page_count + 1

    def parse(self):
        driver = webdriver.Chrome(os.getenv("SELENIUM_ENGINE_PATH"))
        for i in range(1, self.max_page_count):
            driver.get(self.url + f"?p={i}")

        driver.quit()


class AdParser:
    pass


if __name__ == "__main__":
    pagination_parser = PaginationParser(max_page_count=1)
    pagination_parser.parse()
