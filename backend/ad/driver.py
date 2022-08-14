import os
from urllib.parse import urlparse

from autograb.settings import env
import time
import redis
import requests
from selenium import webdriver


def create_driver(mobile=False):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    if mobile:
        mobile_emulation = {"deviceName": "iPhone X"}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    web_driver = webdriver.Chrome(
        options=chrome_options,
    )
    return web_driver


def try_to_get(func):
    count_tries = 0
    while True:
        time.sleep(1)
        try:
            return func()
        except Exception as err:
            print(f"Count Tries: {count_tries}")
            print(err)
        count_tries += 1


def get_session(browser='chrome'):
    data = requests.get(f"{url}/status").json()
    sessions = {
        "chrome": "",
        "firefox": "",
        "edge": "",
    }
    try:
        for node in data['value']['nodes']:
            node_session = node["slots"][0]["session"]
            sessions[node["slots"][0]["stereotype"]["browserName"]] = node_session['sessionId'] if node_session else ""
        return sessions[browser]
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

driver = create_driver()

if int(os.getenv("DOCKER_WORKER", 0)):
    print("WAITING START BACKEND...")
    try_to_get(lambda: requests.get('http://backend:8000/api/grab/'))

session = try_to_get(get_session)

if session:
    print(f"Start Selenium with session ID: {session}")
    driver.command_executor._url = selenium_url.geturl()
    driver.session_id = session
else:
    print("First start, create session...")
    options = webdriver.ChromeOptions()
    options.add_extension("./extension_5_0_4_0.crx")
    driver = try_to_get(
        lambda: webdriver.Remote(
            command_executor=selenium_url.geturl(),
            options=options
        )
    )
    print(f"Success, Selenium session ID: {driver.session_id}")
