import verticallifebot.telegram_utils as telegram_utils
from verticallifebot.logger import logging
from verticallifebot.slot import Slot
from typing import List
import os
from typing import Optional

CHECKINS_URL = os.environ.get('CHECKINS_URL')


class Session:

    def __init__(self, current_day=None):
        self.current_day = current_day
        self.unavailable_slots = set()
        self.silent_update = True

    def reset_day(self, new_day):
        self.current_day = new_day
        self.unavailable_slots.clear()
        self.silent_update = True

    def communicate_availability(self, time):
        message = f"Nuovo slot disponibile per le ore {time}. [Prenota]({CHECKINS_URL})"
        try:
            telegram_utils.send_message(message)
        except Exception:
            logging.error('Error while sending telegram message')

    def communicate_unavailability(self, time):
        message = f"Lo slot delle ore {time} non è più disponibile"
        try:
            telegram_utils.send_message(message)
        except Exception:
            logging.error('Error while sending telegram message')

    def track_changes(self, day: Optional[str], slots: List[Slot]):
        if day is not None and self.current_day != day:
            self.reset_day(day)
        for slot in slots:
            if slot.is_available and slot.time in self.unavailable_slots:
                self.unavailable_slots.remove(slot.time)
                self.communicate_availability(slot.time)
            if not slot.is_available and slot.time not in self.unavailable_slots:
                self.unavailable_slots.add(slot.time)
                if not self.silent_update:
                    self.communicate_unavailability(slot.time)

        if self.silent_update == True: self.silent_update = False