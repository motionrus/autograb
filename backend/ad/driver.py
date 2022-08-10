import os
from urllib.parse import urlparse

import environ
import redis
import requests
from selenium import webdriver


def get_session(data):
    try:
        return data['value']['nodes'][0]['slots'][0]['session']['sessionId']
    except KeyError:
        return ""
    except TypeError:
        return ""
    except IndexError:
        return ""


# INIT REDIS
env = environ.Env()
selenium_url = urlparse(os.getenv("SELENIUM_URL"))

is_selenium_hub = 'hub' in selenium_url.path
redis_env = env.db('REDIS_URL')

redis_cursor = redis.Redis(
    host=redis_env["HOST"],
    port=redis_env["PORT"],
    db=1,
)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.quit()

session = redis_cursor.get("session")
if session:
    session = session.decode()

if is_selenium_hub:
    url = f"{selenium_url.scheme}://{selenium_url.netloc}"
    try:
        status_data = requests.get(f"{url}/status").json()
        session = get_session(status_data)
    except requests.exceptions.ConnectionError:
        pass


if session:
    driver.command_executor._url = selenium_url.geturl()
    driver.session_id = session
else:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_extension("./extension_5_0_4_0.crx")
    driver = webdriver.Remote(
        command_executor=selenium_url.geturl(),
        options=options
    )
    redis_cursor.set("session", driver.session_id)

print(f"Start Selenium Session: {redis_cursor.get('session').decode()}")
