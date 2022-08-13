import os
from urllib.parse import urlparse

from autograb.settings import env
import time
import redis
import requests
from selenium import webdriver


def try_to_get(func):
    count_tries = 0
    while True:
        time.sleep(5)
        try:
            return func()
        except Exception as err:
            print(f"Count Tries: {count_tries}")
            print(err)
        count_tries += 1


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


redis_env = env.db('REDIS_URL')
redis_cursor = redis.Redis(
    host=redis_env["HOST"],
    port=redis_env["PORT"],
    db=1,
)

selenium_url = urlparse(env.get_value("SELENIUM_URL"))
url = f"{selenium_url.scheme}://{selenium_url.netloc}"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.quit()


if int(os.getenv("DOCKER_WORKER", 0)):
    print("WAITING START BACKEND...")
    try_to_get(lambda: requests.get('http://backend:8000/api/grab/'))


session = try_to_get(get_session)


if session:
    driver.command_executor._url = selenium_url.geturl()
    driver.session_id = session
else:
    options = webdriver.ChromeOptions()
    options.add_extension("./extension_5_0_4_0.crx")
    driver = try_to_get(
        lambda: webdriver.Remote(
            command_executor=selenium_url.geturl(),
            options=options
        )
    )

print(f"Start Selenium Session ID: {session}")
