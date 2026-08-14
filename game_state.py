from datetime import date, timedelta
import random

from fire import ignite_tile, extinguish_tile
from simulation import simulate_day


class GameState:
    def __init__(self, forest_map):
        self.forest_map = forest_map
        self.current_date = date(1990, 1, 1)
        self.paused = True
        self.simulation_speed = 1
        self.dryness = 42
        self.active_fire_count = 0
        self.resources = {
            "restore": 2,
            "replant": 3,
            "protect": 1,
        }
        self.selected_tile = None
        self.accumulator = 0.0
        self.last_day = self.current_date

        self.update_fire_count()

    def set_speed(self, speed):
        self.simulation_speed = max(0, speed)
        self.paused = self.simulation_speed == 0

    def pause(self):
        self.paused = True
        self.simulation_speed = 0

    def resume(self):
        self.paused = False
        if self.simulation_speed == 0:
            self.simulation_speed = 1

    def get_selected_tile(self):
        if self.selected_tile is None:
            return None
        x, y = self.selected_tile
        if 0 <= y < len(self.forest_map.tiles) and 0 <= x < len(self.forest_map.tiles[y]):
            return self.forest_map.tiles[y][x]
        return None

    def update_fire_count(self):
        self.active_fire_count = 0
        for row in self.forest_map.tiles:
            for tile in row:
                if tile.fire_active:
                    self.active_fire_count += 1

    def advance_days(self, days=1):
        for _ in range(days):
            self.advance_day()

    def advance_day(self):
        self.current_date += timedelta(days=1)
        simulate_day(self.forest_map, self)
        self.update_fire_count()

    def reset_resources(self):
        base = {"restore": 2, "replant": 3, "protect": 1}
        self.resources = base

    def apply_restore(self):
        tile = self.get_selected_tile()
        if tile is None or self.resources["restore"] <= 0:
            return False
        tile.restore()
        self.resources["restore"] -= 1
        return True

    def apply_replant(self):
        tile = self.get_selected_tile()
        if tile is None or self.resources["replant"] <= 0:
            return False
        tile.replant()
        self.resources["replant"] -= 1
        return True

    def apply_protect(self):
        tile = self.get_selected_tile()
        if tile is None or self.resources["protect"] <= 0:
            return False
        tile.protect()
        self.resources["protect"] -= 1
        return True

    def ignite_selected_tile(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        return ignite_tile(tile, intensity=60)

    def extinguish_selected_tile(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        return extinguish_tile(tile)

    def extinguish_all_fires(self):
        for row in self.forest_map.tiles:
            for tile in row:
                if tile.fire_active:
                    extinguish_tile(tile)
        return True

    def ignite_random_tile(self):
        rows = self.forest_map.tiles
        if not rows:
            return False
        y = random.randrange(len(rows))
        x = random.randrange(len(rows[y]))
        tile = rows[y][x]
        return ignite_tile(tile, intensity=random.randint(30, 80))

    def ignite_random_area(self):
        center_x = random.randrange(self.forest_map.width)
        center_y = random.randrange(self.forest_map.height)
        radius = 2
        ignited = 0
        for y in range(max(0, center_y - radius), min(self.forest_map.height, center_y + radius + 1)):
            for x in range(max(0, center_x - radius), min(self.forest_map.width, center_x + radius + 1)):
                tile = self.forest_map.tiles[y][x]
                if tile.type != "water":
                    ignite_tile(tile, intensity=random.randint(35, 75))
                    ignited += 1
        return ignited > 0

    def damage_selected_tile(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        tile.health = max(0, tile.health - 20)
        tile.biodiversity = max(0, tile.biodiversity - 20)
        tile.degradation = min(100, tile.degradation + 20)
        return True

    def restore_selected_tile(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        tile.restore()
        return True

    def set_selected_tile_healthy(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        tile.health = 100
        tile.biodiversity = 100
        tile.water = 100
        tile.degradation = 0
        tile.fire_risk = 0
        tile.fire_active = False
        tile.burned = False
        tile.recovering = False
        tile.type = "forest"
        return True

    def set_selected_tile_burnt(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        tile.health = 15
        tile.biodiversity = 5
        tile.water = 20
        tile.degradation = 80
        tile.burned = True
        tile.fire_active = True
        tile.fire_intensity = 85
        tile.fire_state = "burning"
        return True
