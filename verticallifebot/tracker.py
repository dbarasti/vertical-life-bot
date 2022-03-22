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

    def track_changes(self, day: Optional[str], slots: List[Slot]):
        if day is not None and self.current_day != day:
            # TODO: move to reset_day()
            self.current_day = day
            self.unavailable_slots.clear()
            self.silent_update = True
        for slot in slots:
            if slot.is_available and slot.time in self.unavailable_slots:
                self.unavailable_slots.remove(slot.time)
                message = f"Nuovo slot disponibile per le ore [{slot.time}]({CHECKINS_URL})"
                try:
                    telegram_utils.send_message(message)
                except Exception:
                    logging.warn('Error while sending telegram message')
            if not slot.is_available and slot.time not in self.unavailable_slots:
                self.unavailable_slots.add(slot.time)
                if not self.silent_update:
                    message = f"Lo slot delle ore {self.time} non è più disponibile"
                    try:
                        telegram_utils.send_message(message)
                    except Exception:
                        logging.warn('Error while sending telegram message')

        if self.silent_update == True: self.silent_update = False