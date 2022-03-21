'''
This module looks for changes in the checkins page.
It keeps track of the available spots. In particular, it there is a change from "Fully booked" to one or more spots available, 
it sends a message on the telegram channel with the appropriate details.
'''
import verticallifebot.telegram_utils as telegram_utils
from verticallifebot.logger import logging
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
    today = ""
    unavailable_slots = set()
    silent_update = True

    while True:
        logging.info("Loading page")
        driver.get(CHECKINS_URL)
        time.sleep(5)
        slots = driver.find_elements_by_xpath(
            "//div[contains(@class, 'row') and contains(@class, 'align-items-center')]"
        )
        if len(slots) > 4:
            # remove useless content
            slots = slots[4:]

            # check if day has changed
            try:
                page_date = slots[0].find_element(by=By.CLASS_NAME,
                                                  value="mb-1").text
            except NoSuchElementException:
                logging.warning('Could not find page date')

            if today != page_date:
                today = page_date
                unavailable_slots.clear()
                silent_update = True

            for slot in slots:
                try:
                    time_slot = slot.find_elements(by=By.CLASS_NAME,
                                                   value="mb-1")[1].text
                except NoSuchElementException:
                    continue
                try:
                    _ = slot.find_element(by=By.CLASS_NAME,
                                          value="badge-danger")
                except NoSuchElementException:
                    if time_slot in unavailable_slots:
                        unavailable_slots.remove(time_slot)
                        message = f"Nuovo slot disponibile per le ore [{time_slot}]({CHECKINS_URL})"
                        try:
                            telegram_utils.send_message(message)
                        except Exception:
                            logging.warn(
                                'Error while sending telegram message')
                    continue
                if time_slot not in unavailable_slots:
                    unavailable_slots.add(time_slot)
                    if not silent_update:
                        message = f"Lo slot delle ore {time_slot} non è più disponibile"
                        try:
                            telegram_utils.send_message(message)
                        except Exception:
                            logging.warn(
                                'Error while sending telegram message')
            silent_update = False
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
