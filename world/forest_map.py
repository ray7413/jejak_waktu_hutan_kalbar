import random

from .tile import Tile


class ForestMap:
    WIDTH = 20
    HEIGHT = 20
    TILE_WIDTH = 80
    TILE_HEIGHT = 40

    def __init__(self):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.tiles = []
        self.selected = None
        self.hover = None
        self.camera_offset = (0, 0)
        self.generate()

    def generate(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                roll = random.random()
                if roll < 0.12:
                    ground = "water"
                elif roll < 0.22:
                    ground = "degraded"
                elif roll < 0.35:
                    ground = "recovering"
                else:
                    ground = "forest"

                tile = Tile(x, y, ground)
                tile.health = 40 + random.randint(0, 55)
                tile.biodiversity = 35 + random.randint(0, 55)
                tile.water = 45 + random.randint(0, 40)
                tile.fire_risk = 8 + random.randint(0, 25)
                tile.dryness = 35 + random.randint(0, 30)
                if ground == "water":
                    tile.health = 20
                    tile.biodiversity = 10
                    tile.water = 90
                    tile.ground_type = "water"
                    tile.vegetation_type = "none"
                elif ground == "degraded":
                    tile.health = 52
                    tile.biodiversity = 42
                    tile.vegetation_type = random.choice(["grass", "bush", "tree_small"])
                elif ground == "recovering":
                    tile.health = 62
                    tile.biodiversity = 55
                    tile.vegetation_type = random.choice(["grass", "bush", "tree_small", "tree_standard"])
                else:
                    choices = ["tree_standard", "tree_palm", "grass", "bush", "tree_small"]
                    weights = [2, 1, 3, 2, 3]
                    tile.vegetation_type = random.choices(choices, weights=weights, k=1)[0]
                row.append(tile)
            self.tiles.append(row)

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def get_neighbors(self, tile):
        neighbors = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx = tile.x + dx
                ny = tile.y + dy
                neighbor = self.get_tile(nx, ny)
                if neighbor is not None:
                    neighbors.append(neighbor)
        return neighbors

    def select_tile(self, x, y):
        tile = self.get_tile(x, y)
        self.selected = tile
        return tile

    def get_selected_tile(self):
        return self.selected

    def set_hover(self, x, y):
        self.hover = self.get_tile(x, y)

    def get_tile_at_screen(self, screen_x, screen_y, camera):
        for row in self.tiles:
            for tile in row:
                sx, sy = camera.world_to_screen(tile.x, tile.y)
                half_w = 40 * camera.zoom
                half_h = 20 * camera.zoom
                dx = screen_x - sx
                dy = screen_y - sy
                if abs(dx) <= half_w and abs(dy) <= half_h:
                    if abs(dx) / half_w + abs(dy) / half_h <= 1.25:
                        return tile
        return None

    def stats(self):
        count = 0
        health_total = 0
        biodiversity_total = 0
        water_total = 0
        forest_total = 0
        degraded_total = 0
        burnt_total = 0
        recovering_total = 0
        fire_count = 0
        for row in self.tiles:
            for tile in row:
                if tile.ground_type == "water":
                    continue
                count += 1
                health_total += tile.health
                biodiversity_total += tile.biodiversity
                water_total += tile.water
                if tile.ground_type == "forest":
                    forest_total += 1
                if tile.ground_type == "degraded":
                    degraded_total += 1
                if tile.burnt:
                    burnt_total += 1
                if tile.ground_type == "recovering":
                    recovering_total += 1
                if tile.fire_active:
                    fire_count += 1
        if count == 0:
            return {
                "health": 0,
                "biodiversity": 0,
                "water": 0,
                "forest": 0,
                "degraded": 0,
                "burnt": 0,
                "recovering": 0,
                "fires": 0,
            }
        return {
            "health": round(health_total / count, 1),
            "biodiversity": round(biodiversity_total / count, 1),
            "water": round(water_total / count, 1),
            "forest": round(forest_total / count * 100, 1),
            "degraded": degraded_total,
            "burnt": burnt_total,
            "recovering": recovering_total,
            "fires": fire_count,
        }
