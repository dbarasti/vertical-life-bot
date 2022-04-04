class Slot:

    def __init__(self, time, is_available):
        if ':' not in time:
            return None
        self.time = time
        self.is_available = is_available
