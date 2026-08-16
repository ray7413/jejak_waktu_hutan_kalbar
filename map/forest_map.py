import pygame
import random

from .tiles import Tile

from config import (
    MAP_WIDTH,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_ZOOM_MIN,
    MAP_ZOOM_MAX,
    TILE_WIDTH,
    TILE_HEIGHT
)

from assets.assets import (
    forest,
    degraded,
    burnt,
    recovering,
    water
)

class ForestMap:

    def __init__(self):

        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.offset_x = MAP_OFFSET_X
        self.offset_y = MAP_OFFSET_Y

        self.zoom = 1
        self.min_zoom = MAP_ZOOM_MIN
        self.max_zoom = MAP_ZOOM_MAX

        self.tiles = []

        self.generate()

    # generate map
    def generate(self):
        self.tiles = []

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


    # translate grid to xy coords

    def grid_to_screen(self, x, y):

        cx = self.offset_x + (x - y) * (TILE_WIDTH // 2) * self.zoom
        cy = self.offset_y + (x + y) * (TILE_HEIGHT // 2) * self.zoom

        return cx, cy

    def draw(self, screen):

        for y in range(self.height):

            for x in range(self.width):

                tile = self.tiles[y][x]

                cx, cy = self.grid_to_screen(x, y)

                img = tile.get_type()
                if img is None:
                    continue

                image = {
                    "forest": forest,
                    "recovering": recovering,
                    "degraded": degraded,
                    "water": water,
                    "burnt": burnt,
                }.get(tile.type)

                if image is None:
                    continue

                scaled_w = max(1, int(image.get_width() * self.zoom))
                scaled_h = max(1, int(image.get_height() * self.zoom))
                scaled_img = pygame.transform.smoothscale(
                    image,
                    (scaled_w, scaled_h)
                )

                screen.blit(
                    scaled_img,
                    (cx - scaled_w // 2, cy - scaled_h // 2)
                )

    # locate selected tile 

    def get_tile_at_mouse(self, mouse_pos):

        mouse_x, mouse_y = mouse_pos

        for y in range(self.height):

            for x in range(self.width):

                cx, cy = self.grid_to_screen(x, y)

                dx = abs(mouse_x - cx)
                dy = abs(mouse_y - cy)

                tile = self.tiles[y][x]
                tile_type = tile.get_type()
                image = {
                    "forest": forest,
                    "recovering": recovering,
                    "degraded": degraded,
                    "water": water,
                    "burnt": burnt,
                }.get(tile_type)
                if image is None:
                    continue

                half_w = (image.get_width() * self.zoom) / 2
                half_h = (image.get_height() * self.zoom) / 2

                if half_w <= 0 or half_h <= 0:
                    continue

                if (dx / half_w + dy / half_h) <= 1:
                    return x, y

        return None
