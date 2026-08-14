import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND
)

from config import load_assets

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

load_assets()


# =========================
# GAME OBJECTS
# =========================

forest_map = ForestMap()

sidebar = Sidebar()

year = 1

selected_tile = None

# Dragging state for right mouse pan
dragging = False
_drag_start_mouse = (0, 0)
_drag_start_offset = (0, 0)

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

            # Left click: select tile
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

            # Right click: start dragging/panning
            elif event.button == 3:
                dragging = True
                _drag_start_mouse = event.pos
                _drag_start_offset = (forest_map.offset_x, forest_map.offset_y)

        # Mouse button released
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                dragging = False

        # Mouse motion: if dragging update offsets
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                mx, my = event.pos
                sx, sy = _drag_start_mouse
                dx = mx - sx
                dy = my - sy
                forest_map.offset_x = _drag_start_offset[0] + dx
                forest_map.offset_y = _drag_start_offset[1] + dy

        # Mouse wheel: zoom in/out
        if event.type == pygame.MOUSEWHEEL:
            forest_map.set_zoom(
                forest_map.zoom + (event.y * 0.1),
                pygame.mouse.get_pos()
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

        tile_img = forest_map.tiles[y][x].get_type()
        half_w = tile_img.get_width() * forest_map.zoom / 2 if tile_img else 32
        half_h = tile_img.get_height() * forest_map.zoom / 2 if tile_img else 16

        points = [
            (cx, cy - half_h),
            (cx + half_w, cy),
            (cx, cy + half_h),
            (cx - half_w, cy)
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