'''
This module looks for changes in the checkins page.
It keeps track of the available spots. In particular, it there is a change from "Fully booked" to one or more spots available, 
it sends a message on the telegram channel with the appropriate details.
'''
import telegram_utils
from logger import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

CHECKINS_URL = os.environ.get('CHECKINS_URL')


def launch():
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    today = ""
    unavailable_slots = set()
    silent_update = True

    while True:
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
                logging.warning('could not find page date')

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
                    if time_slot not in unavailable_slots:
                        unavailable_slots.add(time_slot)
                        if not silent_update:
                            message = f"Lo slot delle ore {time_slot} non è più disponibile"
                            try:
                                telegram_utils.send_message(message)
                            except Exception:
                                logging.error(
                                    'error while sending telegram message')
                except NoSuchElementException:
                    if time_slot in unavailable_slots:
                        unavailable_slots.remove(time_slot)
                        message = f"Nuovo slot disponibile per le ore {time_slot}"
                        try:
                            telegram_utils.send_message(message)
                        except Exception:
                            logging.error(
                                'error while sending telegram message')
                    continue
            silent_update = False
        time.sleep(120)