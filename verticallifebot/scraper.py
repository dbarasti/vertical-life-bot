'''
This module periodically polls the booking page, each time sending the page to the slot module.
'''
from verticallifebot.logger import logging
import verticallifebot.handler as handler
import time
import sys
import os

from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions

CHECKINS_URL = os.environ.get('CHECKINS_URL')
TEST = os.environ.get('TEST')
if TEST == 'True':
    UPDATE_INTERVAL = 5
else:
    UPDATE_INTERVAL = 120


def launch():
    try:
        driver = setup_driver()
    except:
        logging.error("Unable to create driver. Shutting down...")
        sys.exit()

    while True:
        logging.info("Loading page")
        try:
            driver.get(CHECKINS_URL)
        except Exception:
            logging.warn("Unable to get page. Will retry next time")
            time.sleep(UPDATE_INTERVAL)
            continue
        time.sleep(5)

        # send slots to handler module
        try:
            handler.handle_page(driver)
        except Exception:
            logging.error("Error while parsing page")

        time.sleep(UPDATE_INTERVAL)


def setup_driver():
    logging.info("Setting up driver")
    options = ChromiumOptions()
    options.headless = True
    options.add_argument("enable-automation")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)
    return driver
