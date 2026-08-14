import config


class Tile:

    def __init__(self, tile_type="forest"):
        self.type = tile_type

        self.health = 100
        self.biodiversity = 100
        self.soil = 100
        self.water = 100

    def get_type(self):

        if self.type == "forest":
            return config.FOREST

        if self.type == "recovering":
            return config.RECOVERING

        if self.type == "degraded":
            return config.DEGRADED

        if self.type == "water":
            return config.WATER

        return config.FOREST