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

    def get_type(self):
        return self.type