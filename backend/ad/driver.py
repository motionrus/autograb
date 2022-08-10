import os
from urllib.parse import urlparse

import environ
import time
import redis
import requests
from selenium import webdriver


def try_to_get(func):
    count_tries = 5
    while count_tries:
        time.sleep(5)
        try:
            return func()
        except Exception as err:
            print(f"Count Tries Left: {count_tries}")
            print(err)
        count_tries -= 1


def get_session():
    data = requests.get(f"{url}/status").json()
    try:
        return data['value']['nodes'][0]['slots'][0]['session']['sessionId']
    except KeyError:
        return ""
    except TypeError:
        return ""
    except IndexError:
        return ""


env = environ.Env()
redis_env = env.db('REDIS_URL')
redis_cursor = redis.Redis(
    host=redis_env["HOST"],
    port=redis_env["PORT"],
    db=1,
)

selenium_url = urlparse(os.getenv("SELENIUM_URL"))
url = f"{selenium_url.scheme}://{selenium_url.netloc}"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.quit()

session = try_to_get(get_session)

if session:
    driver.command_executor._url = selenium_url.geturl()
    driver.session_id = session
else:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_extension("./extension_5_0_4_0.crx")
    driver = try_to_get(
        lambda: webdriver.Remote(
            command_executor=selenium_url.geturl(),
            options=options
        )
    )

print(f"Start Selenium Session ID: {session}")
