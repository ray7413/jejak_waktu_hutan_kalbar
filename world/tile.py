class Tile:
    def __init__(self, x, y, ground_type="forest"):
        self.x = x
        self.y = y
        self.ground_type = ground_type
        self.vegetation_type = "tree_standard"
        self.health = 85
        self.biodiversity = 75
        self.water = 65
        self.fire_risk = 12
        self.fire_active = False
        self.fire_intensity = 0
        self.fire_age = 0
        self.fire_state = "NORMAL"
        self.protected = False
        self.firebreak = False
        self.firebreak_progress = 0
        self.firebreak_active = False
        self.monitored = False
        self.recovery_progress = 0
        self.forest_age = 12
        self.dryness = 40
        self.burnt = False

    def clone(self):
        tile = Tile(self.x, self.y, self.ground_type)
        for key, value in self.__dict__.items():
            setattr(tile, key, value)
        return tile

    def set_ground_from_state(self):
        if self.ground_type == "water":
            return
        if self.fire_active:
            self.ground_type = "burnt"
        elif self.health < 35 or self.burnt:
            self.ground_type = "burnt"
        elif self.health < 60:
            self.ground_type = "recovering"
        elif self.health < 75:
            self.ground_type = "degraded"
        else:
            self.ground_type = "forest"

    def apply_damage(self, amount):
        self.health = max(0, self.health - amount)
        self.biodiversity = max(0, self.biodiversity - amount * 0.7)
        self.water = max(0, self.water - amount * 0.5)
        self.fire_risk = min(100, self.fire_risk + amount * 0.5)
        self.set_ground_from_state()

    def replant(self):
        self.health = min(100, self.health + 18)
        self.biodiversity = min(100, self.biodiversity + 14)
        self.water = min(100, self.water + 8)
        self.recovery_progress = min(100, self.recovery_progress + 30)
        self.burnt = False
        self.set_ground_from_state()

    def restore_water(self):
        self.water = min(100, self.water + 18)
        self.fire_risk = max(0, self.fire_risk - 10)

    def protect(self):
        self.protected = True
        self.fire_risk = max(0, self.fire_risk - 12)
        self.biodiversity = min(100, self.biodiversity + 6)

    def monitor(self):
        self.monitored = True

    def get_state_label(self):
        if self.ground_type == "water":
            return "Water"
        if self.fire_active:
            return "Burning"
        if self.burnt:
            return "Burnt"
        if self.ground_type == "recovering":
            return "Recovering"
        if self.ground_type == "degraded":
            return "Degraded"
        if self.ground_type == "forest":
            return "Forest"
        return "Forest"

    def summary(self):
        return {
            "x": self.x,
            "y": self.y,
            "ground_type": self.ground_type,
            "health": round(self.health, 1),
            "biodiversity": round(self.biodiversity, 1),
            "water": round(self.water, 1),
            "fire_active": self.fire_active,
            "fire_intensity": self.fire_intensity,
            "protected": self.protected,
        }
