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

        # Mutable offsets so the map can be panned/dragged at runtime
        self.offset_x = MAP_OFFSET_X
        self.offset_y = MAP_OFFSET_Y

        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.5

        self.tiles = []

        self.generate()

    # -------------------------
    # Generate map
    # -------------------------

    def generate(self):

        for y in range(self.height):

            row = []

            for x in range(self.width):

                roll = random.random()

                if roll < 0.80:
                    tile_type = "forest"

                elif roll < 0.90:
                    tile_type = "recovering"

                elif roll < 0.96:
                    tile_type = "degraded"

                else:
                    tile_type = "water"

                row.append(Tile(tile_type))

            self.tiles.append(row)

    # -------------------------
    # Grid → Screen
    # -------------------------

    def grid_to_screen(self, x, y):

        # Use instance offsets and zoom so the map can be panned and zoomed at runtime
        screen_x = self.offset_x + (x - y) * (TILE_WIDTH // 2) * self.zoom

        screen_y = self.offset_y + (x + y) * (TILE_HEIGHT // 2) * self.zoom

        return screen_x, screen_y

    def set_zoom(self, zoom, center):
        mouse_x, mouse_y = center

        old_zoom = self.zoom
        new_zoom = max(self.min_zoom, min(self.max_zoom, zoom))

        if new_zoom == old_zoom:
            return

        # Keep the map position stable under the mouse cursor while zooming
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

                # Skip if assets not loaded yet
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

                if (dx / half_w + dy / half_h) <= 1:
                    return x, y

        return None