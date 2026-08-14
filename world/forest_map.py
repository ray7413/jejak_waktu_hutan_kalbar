import random
import pygame

from config import (
    MAP_WIDTH,
    MAP_HEIGHT,
    TILE_WIDTH,
    TILE_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    GRID
)

from .tile import Tile


class ForestMap:

    def __init__(self):

        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.offset_x = MAP_OFFSET_X
        self.offset_y = MAP_OFFSET_Y

        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.5

        self.tiles = []

        self.generate()
        self.refresh_tile_states()

    # -------------------------
    # Generate map
    # -------------------------

    def generate(self):

        for y in range(self.height):

            row = []

            for x in range(self.width):

                roll = random.random()

                if roll < 0.75:
                    tile_type = "forest"
                elif roll < 0.88:
                    tile_type = "recovering"
                elif roll < 0.97:
                    tile_type = "degraded"
                else:
                    tile_type = "water"

                tile = Tile(tile_type)
                if tile_type == "forest":
                    tile.health = 85 + random.randint(0, 15)
                    tile.biodiversity = 80 + random.randint(0, 15)
                    tile.water = 75 + random.randint(0, 20)
                elif tile_type == "recovering":
                    tile.health = 60 + random.randint(0, 20)
                    tile.biodiversity = 50 + random.randint(0, 25)
                    tile.water = 60 + random.randint(0, 20)
                    tile.recovering = True
                elif tile_type == "degraded":
                    tile.health = 40 + random.randint(0, 25)
                    tile.biodiversity = 35 + random.randint(0, 25)
                    tile.water = 50 + random.randint(0, 25)
                    tile.degradation = 35 + random.randint(0, 30)
                else:
                    tile.health = 20
                    tile.biodiversity = 15
                    tile.water = 50

                row.append(tile)

            self.tiles.append(row)

    def refresh_tile_states(self):
        for row in self.tiles:
            for tile in row:
                if tile.type == "water":
                    continue
                tile.update_visual_state()

    def natural_recovery_step(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                if tile.type == "water":
                    continue

                if tile.protection_turns > 0:
                    tile.protection_turns -= 1
                    tile.fire_risk = max(0, tile.fire_risk - 5)

                healthy_neighbors = 0
                for ny in range(max(0, y - 1), min(self.height, y + 2)):
                    for nx in range(max(0, x - 1), min(self.width, x + 2)):
                        if nx == x and ny == y:
                            continue
                        neighbor = self.tiles[ny][nx]
                        if neighbor.type != "water" and neighbor.health > 70 and not neighbor.burned:
                            healthy_neighbors += 1

                if tile.burned:
                    tile.health = max(0, tile.health - 4)
                    tile.biodiversity = max(0, tile.biodiversity - 3)
                    if tile.health > 55:
                        tile.burned = False
                        tile.recovering = True
                    continue

                if tile.health < 100:
                    gain = 0.8 + (tile.water / 100) * 1.2 + (tile.biodiversity / 100) * 0.8 + (healthy_neighbors * 0.15)
                    tile.health = min(100, tile.health + gain)
                    tile.biodiversity = min(100, tile.biodiversity + gain * 0.6)
                    tile.water = min(100, tile.water + gain * 0.3)
                    tile.degradation = max(0, tile.degradation - gain * 0.7)
                    tile.fire_risk = max(0, tile.fire_risk - gain * 0.2)

                if tile.health > 60 and tile.degradation <= 15:
                    tile.recovering = False
                elif tile.health < 80:
                    tile.recovering = True

                tile.update_visual_state()

    def get_global_stats(self):
        forest_tiles = []
        for row in self.tiles:
            for tile in row:
                if tile.type != "water":
                    forest_tiles.append(tile)

        if not forest_tiles:
            return {
                "health": 0,
                "biodiversity": 0,
                "water": 0,
                "coverage": 0,
                "degraded": 0,
                "burned": 0,
                "recovering": 0,
            }

        total_health = sum(tile.health for tile in forest_tiles)
        total_biodiversity = sum(tile.biodiversity for tile in forest_tiles)
        total_water = sum(tile.water for tile in forest_tiles)

        forest_coverage = sum(1 for tile in forest_tiles if tile.type == "forest")
        degraded_area = sum(1 for tile in forest_tiles if tile.type == "degraded")
        burned_area = sum(1 for tile in forest_tiles if tile.burned)
        recovering_area = sum(1 for tile in forest_tiles if tile.recovering and not tile.burned)

        return {
            "health": round(total_health / len(forest_tiles), 1),
            "biodiversity": round(total_biodiversity / len(forest_tiles), 1),
            "water": round(total_water / len(forest_tiles), 1),
            "coverage": round((forest_coverage / len(forest_tiles)) * 100, 1),
            "degraded": degraded_area,
            "burned": burned_area,
            "recovering": recovering_area,
        }

    # -------------------------
    # Grid → Screen
    # -------------------------

    def grid_to_screen(self, x, y):

        screen_x = self.offset_x + (x - y) * (TILE_WIDTH // 2) * self.zoom
        screen_y = self.offset_y + (x + y) * (TILE_HEIGHT // 2) * self.zoom

        return screen_x, screen_y

    def set_zoom(self, zoom, center):
        mouse_x, mouse_y = center

        old_zoom = self.zoom
        new_zoom = max(self.min_zoom, min(self.max_zoom, zoom))

        if new_zoom == old_zoom:
            return

        world_x = (mouse_x - self.offset_x) / old_zoom
        world_y = (mouse_y - self.offset_y) / old_zoom

        self.zoom = new_zoom
        self.offset_x = mouse_x - world_x * new_zoom
        self.offset_y = mouse_y - world_y * new_zoom

    # -------------------------
    # Draw
    # -------------------------

    def draw(self, screen):

        for y in range(self.height):

            for x in range(self.width):

                tile = self.tiles[y][x]

                cx, cy = self.grid_to_screen(x, y)

                img = tile.get_type()

                if img is None:
                    continue

                scaled_w = max(1, int(img.get_width() * self.zoom))
                scaled_h = max(1, int(img.get_height() * self.zoom))
                scaled_img = pygame.transform.smoothscale(
                    img,
                    (scaled_w, scaled_h)
                )

                screen.blit(
                    scaled_img,
                    (cx - scaled_w // 2, cy - scaled_h // 2)
                )

                if tile.fire_active:
                    flame_size = max(10, int(16 * self.zoom))
                    flame_points = [
                        (cx, cy - flame_size),
                        (cx + flame_size * 0.8, cy - flame_size * 0.3),
                        (cx + flame_size * 0.5, cy + flame_size * 0.7),
                        (cx, cy + flame_size),
                        (cx - flame_size * 0.5, cy + flame_size * 0.5),
                        (cx - flame_size * 0.7, cy - flame_size * 0.2),
                    ]
                    pygame.draw.polygon(screen, (255, 120, 20), flame_points)
                    pygame.draw.polygon(screen, (255, 220, 60), [
                        (cx, cy - flame_size * 0.7),
                        (cx + flame_size * 0.45, cy - flame_size * 0.15),
                        (cx, cy + flame_size * 0.5)
                    ])

    # -------------------------
    # Find tile under mouse
    # -------------------------

    def get_tile_at_mouse(self, mouse_pos):

        mouse_x, mouse_y = mouse_pos

        for y in range(self.height):

            for x in range(self.width):

                cx, cy = self.grid_to_screen(x, y)

                dx = abs(mouse_x - cx)
                dy = abs(mouse_y - cy)

                img = self.tiles[y][x].get_type()
                if img is None:
                    continue

                half_w = (img.get_width() * self.zoom) / 2
                half_h = (img.get_height() * self.zoom) / 2

                if half_w <= 0 or half_h <= 0:
                    continue

                if (dx / half_w + dy / half_h) <= 1:
                    return x, y

        return None