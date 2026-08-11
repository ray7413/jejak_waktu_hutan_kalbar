import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND
)

from world.forest_map import ForestMap
from ui.sidebar import Sidebar


# =========================
# INITIALIZATION
# =========================

pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "Jejak Waktu"
)

clock = pygame.time.Clock()


# =========================
# GAME OBJECTS
# =========================

forest_map = ForestMap()

sidebar = Sidebar()

year = 1

selected_tile = None


# =========================
# GAME LOOP
# =========================

running = True

while running:

    # ---------------------
    # EVENTS
    # ---------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse click

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                selected_tile = (
                    forest_map.get_tile_at_mouse(
                        event.pos
                    )
                )

                if selected_tile:

                    x, y = selected_tile

                    tile = forest_map.tiles[y][x]

                    print(
                        f"Tile ({x}, {y})"
                    )

                    print(
                        f"Type: {tile.type}"
                    )

                    print(
                        f"Health: {tile.health}"
                    )


    # ---------------------
    # DRAW
    # ---------------------

    screen.fill(BACKGROUND)

    forest_map.draw(screen)

    sidebar.draw(
        screen,
        year
    )

    # ---------------------
    # Selected tile
    # ---------------------

    if selected_tile:

        x, y = selected_tile

        cx, cy = forest_map.grid_to_screen(
            x,
            y
        )

        points = [
            (cx, cy - 16),
            (cx + 32, cy),
            (cx, cy + 16),
            (cx - 32, cy)
        ]

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            points,
            3
        )


    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()