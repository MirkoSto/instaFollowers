import json
import time

from selenium import webdriver
from configuration import Configuration


class WebDriverInstance:

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_experimental_option("detach", True) #promeniti na False ili izbrisati, u production fazi
        options.add_argument("--window-size=1550,600")
        options.add_argument("--lang=en")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-application-cache")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)

        options.add_argument('--disable-blink-features=AutomationControlled')

        self.driver = webdriver.Chrome(options=options, executable_path=Configuration.CHROMEDRIVER_PATH)


