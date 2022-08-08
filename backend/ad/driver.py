import os
from selenium import webdriver
import redis, environ

# INIT REDIS
env = environ.Env()
redis_env = env.db('REDIS_URL')

redis_cursor = redis.Redis(
    host=redis_env["HOST"],
    port=redis_env["PORT"],
    db=1,
)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_extension("./extension_5_0_4_0.crx")

driver = webdriver.Chrome(options=options)
session = redis_cursor.get("session").decode()

if session:
    driver.command_executor._url = os.getenv("SELENIUM_URL")
    driver.session_id = session
else:
    driver = webdriver.Remote(
        command_executor=os.getenv("SELENIUM_URL"),
        options=options
    )
    redis_cursor.set("session", driver.session_id)


print(driver.command_executor._url)
print(driver.session_id)
