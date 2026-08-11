from config import FOREST, RECOVERING, DEGRADED, WATER


class Tile:

    def __init__(self, tile_type="forest"):
        self.type = tile_type

        self.health = 100
        self.biodiversity = 100
        self.soil = 100
        self.water = 100

    def get_color(self):

        if self.type == "forest":
            return FOREST

        if self.type == "recovering":
            return RECOVERING

        if self.type == "degraded":
            return DEGRADED

        if self.type == "water":
            return WATER

        return FOREST