from datetime import date, timedelta


class TimeSystem:
    START_DATE = date(1990, 1, 1)

    def __init__(self):
        self.current_date = self.START_DATE
        self.speed = 1
        self.paused = True
        self.accumulator = 0.0

    def set_speed(self, speed):
        self.speed = max(0, int(speed))
        self.paused = self.speed == 0

    def pause(self):
        self.paused = True
        self.speed = 0

    def resume(self):
        self.paused = False
        if self.speed == 0:
            self.speed = 1

    def advance_days(self, days):
        self.current_date += timedelta(days=max(0, days))

    def advance_one_day(self):
        self.advance_days(1)
