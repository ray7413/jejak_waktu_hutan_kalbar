import config


class Tile:

    def __init__(self, tile_type="forest"):
        self.type = tile_type

        self.health = 100
        self.biodiversity = 100
        self.soil = 100
        self.water = 100
        self.forest_age = 25 if tile_type == "forest" else 0
        self.degradation = 0
        self.fire_risk = 10
        self.fire_active = False
        self.fire_intensity = 0
        self.fire_age = 0
        self.fire_fuel = 0
        self.fire_state = "normal"
        self.burned = False
        self.recovering = False
        self.protection_turns = 0
        self.vegetation = "dense"
        self.human_pressure = 20
        self.x = 0
        self.y = 0

    @staticmethod
    def clamp(value, low=0, high=100):
        return max(low, min(high, value))

    def update_visual_state(self):
        if self.type == "water":
            return

        if self.burned:
            self.type = "degraded"
            self.recovering = True
            self.vegetation = "dead"
            return

        if self.degradation >= 60 or self.health <= 25:
            self.type = "degraded"
            self.vegetation = "sparse"
            self.recovering = self.health > 35
            return

        if self.recovering or self.health < 75:
            self.type = "recovering"
            self.vegetation = "regrowing"
            return

        self.type = "forest"
        self.vegetation = "dense" if self.biodiversity > 70 else "normal"
        self.recovering = False

    def get_state_label(self):
        if self.type == "water":
            return "Water"
        if self.burned:
            return "Burned"
        if self.degradation >= 60:
            return "Severely Degraded"
        if self.recovering:
            return "Recovering"
        if self.type == "degraded":
            return "Degraded"
        if self.type == "forest":
            return "Forest"
        return "Forest"

    def restore(self):
        self.health = self.clamp(self.health + 18)
        self.biodiversity = self.clamp(self.biodiversity + 12)
        self.water = self.clamp(self.water + 10)
        self.degradation = max(0, self.degradation - 20)
        self.fire_risk = max(0, self.fire_risk - 15)
        self.burned = False
        self.recovering = True
        self.forest_age = max(self.forest_age, 5)
        self.update_visual_state()

    def replant(self):
        self.health = self.clamp(self.health + 12)
        self.biodiversity = self.clamp(self.biodiversity + 16)
        self.water = self.clamp(self.water + 5)
        self.degradation = max(0, self.degradation - 10)
        self.forest_age = max(1, self.forest_age)
        self.burned = False
        self.recovering = True
        self.update_visual_state()

    def protect(self):
        self.protection_turns = max(self.protection_turns, 3)
        self.fire_risk = max(0, self.fire_risk - 20)
        self.human_pressure = max(0, self.human_pressure - 15)
        self.update_visual_state()

    def ignite(self, intensity=45):
        if self.type == "water":
            return False
        self.fire_active = True
        self.fire_intensity = self.clamp(intensity)
        self.fire_age = 0
        self.fire_fuel = max(10, self.biodiversity * 0.8)
        self.fire_state = "ignited"
        self.burned = False
        self.recovering = True
        self.health = max(0, self.health - 10)
        self.biodiversity = max(0, self.biodiversity - 8)
        return True

    def extinguish(self):
        self.fire_active = False
        self.fire_intensity = 0
        self.fire_age = 0
        self.fire_fuel = 0
        self.fire_state = "extinguished"
        self.burned = self.health <= 35
        return True

    def get_type(self):

        if self.type == "forest":
            return config.FOREST

        if self.type == "recovering":
            return config.RECOVERING

        if self.type in ("degraded", "severely_degraded", "burnt"):
            return config.DEGRADED

        if self.type == "water":
            return config.WATER

        return config.FOREST