import os
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_extension("./extension_5_0_4_0.crx")
driver = webdriver.Remote(
    command_executor=os.getenv("SELENIUM_URL"),
    options=options
)
