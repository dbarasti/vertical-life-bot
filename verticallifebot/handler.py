from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from verticallifebot.slot import Slot
from verticallifebot.tracker import Session
from verticallifebot.logger import logging
from typing import Optional

session = Session()


def handle_page(driver: webdriver):
    raw_slots = driver.find_elements_by_xpath(
        "//div[contains(@class, 'row') and contains(@class, 'align-items-center')]"
    )
    if len(raw_slots) > 4:
        # remove useless content
        raw_slots = raw_slots[4:]
    else:
        raise ValueError("Invalid page content")
    make_slots(raw_slots)


def make_slots(raw_slots):
    slots = []
    for raw_slot in raw_slots:
        time_slot = raw_slot.find_elements(by=By.CLASS_NAME,
                                           value="mb-1")[1].text
        slot_unavailable = check_exists_by_class(raw_slot, "badge-danger")
        slot_obj = Slot(time_slot, not slot_unavailable)
        if slot_obj is None:
            continue
        else:
            slots.append(slot_obj)
    today = extract_day(raw_slots)
    session.track_changes(today, slots)


def check_exists_by_class(driver, class_name):
    try:
        driver.find_element(by=By.CLASS_NAME, value=class_name)
    except NoSuchElementException:
        return False
    return True


def extract_day(raw_slots) -> Optional[str]:
    try:
        page_date = raw_slots[0].find_element(by=By.CLASS_NAME,
                                              value="mb-1").text
    except NoSuchElementException:
        logging.warning('Could not find page date')
    return page_date
