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

        screen_x = MAP_OFFSET_X + (x - y) * (TILE_WIDTH // 2)

        screen_y = MAP_OFFSET_Y + (x + y) * (TILE_HEIGHT // 2)

        return screen_x, screen_y

    # -------------------------
    # Draw
    # -------------------------

    def draw(self, screen):

        for y in range(self.height):

            for x in range(self.width):

                tile = self.tiles[y][x]

                cx, cy = self.grid_to_screen(x, y)

                points = [
                    (cx, cy - TILE_HEIGHT // 2),
                    (cx + TILE_WIDTH // 2, cy),
                    (cx, cy + TILE_HEIGHT // 2),
                    (cx - TILE_WIDTH // 2, cy)
                ]

                pygame.draw.polygon(
                    screen,
                    tile.get_color(),
                    points
                )

                pygame.draw.polygon(
                    screen,
                    GRID,
                    points,
                    1
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

                # Diamond collision
                if (
                    dx / (TILE_WIDTH / 2)
                    +
                    dy / (TILE_HEIGHT / 2)
                    <= 1
                ):

                    return x, y

        return None