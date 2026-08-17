class Environment:
    WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    def __init__(self):
        self.dryness = 42
        self.rainfall = 15
        self.water_availability = 60
        self.wind = "E"

    def apply_daily(self):
        self.rainfall = max(0, min(100, self.rainfall + (10 if self.dryness > 60 else -4)))
        self.water_availability = max(0, min(100, self.water_availability + (10 if self.rainfall > 50 else -6)))
        self.dryness = max(0, min(100, self.dryness + (3 if self.water_availability < 45 else -2)))

        if self.rainfall > 55:
            self.wind = self.WIND_DIRECTIONS[(self.WIND_DIRECTIONS.index(self.wind) + 1) % len(self.WIND_DIRECTIONS)]

    def increase_dryness(self, amount=10):
        self.dryness = max(0, min(100, self.dryness + amount))

    def decrease_dryness(self, amount=10):
        self.dryness = max(0, min(100, self.dryness - amount))

    def trigger_rain(self):
        self.rainfall = min(100, self.rainfall + 35)
        self.water_availability = min(100, self.water_availability + 30)
        self.dryness = max(0, self.dryness - 20)

    def set_wind(self, direction):
        if direction in self.WIND_DIRECTIONS:
            self.wind = direction

    def rotate_wind(self, step):
        index = self.WIND_DIRECTIONS.index(self.wind)
        self.wind = self.WIND_DIRECTIONS[(index + step) % len(self.WIND_DIRECTIONS)]
