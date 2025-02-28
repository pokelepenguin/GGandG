import time

class TimeTracker:
    def __init__(self):
        self.month = 1
        self.year = 0
        self.last_update = time.time()

    def advance_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1

    def get_current_time(self):
        return f"Year: {self.year}, Month: {self.month}"

    def update(self):
        current_time = time.time()
        if current_time - self.last_update >= 5:
            self.advance_month()
            self.last_update = current_time

time_tracker = TimeTracker()
