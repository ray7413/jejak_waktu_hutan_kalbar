import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND
)

from config import load_assets
from debug_menu import DebugMenu
from game_state import GameState
from ui.sidebar import Sidebar
from world.forest_map import ForestMap


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
game = GameState(forest_map)
debug_menu = DebugMenu()

# Dragging state for right mouse pan
dragging = False
_drag_start_mouse = (0, 0)
_drag_start_offset = (0, 0)

# =========================
# GAME LOOP
# =========================

running = True

while running:

    dt = clock.tick(FPS) / 1000.0
    if not game.paused and game.simulation_speed > 0:
        game.accumulator += dt * game.simulation_speed
        while game.accumulator >= 1.0:
            game.advance_day()
            game.accumulator -= 1.0

    # ---------------------
    # EVENTS
    # ---------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.paused:
                    game.resume()
                else:
                    game.pause()
            elif event.key == pygame.K_ESCAPE:
                if debug_menu.visible:
                    debug_menu.visible = False
                else:
                    game.selected_tile = None
            elif event.key == pygame.K_r:
                game.apply_restore()
            elif event.key == pygame.K_p:
                game.apply_replant()
            elif event.key == pygame.K_t:
                game.apply_protect()
            elif event.key == pygame.K_n:
                game.advance_days(1)

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if debug_menu.visible:
                if debug_menu.handle_click(event.pos, game, forest_map):
                    continue
                if event.button == 1:
                    debug_menu.visible = False
                    continue

            hud_click = sidebar.handle_click(event.pos, game)
            if hud_click == "MENU":
                debug_menu.toggle()
                continue
            if hud_click is not None:
                continue

            if event.button == 1:
                selected_tile = forest_map.get_tile_at_mouse(event.pos)
                game.selected_tile = selected_tile
                if selected_tile:
                    x, y = selected_tile
                    tile = forest_map.tiles[y][x]
                    print(f"Tile ({x}, {y}) - {tile.get_state_label()}")

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

    if game.selected_tile:
        x, y = game.selected_tile
        cx, cy = forest_map.grid_to_screen(x, y)
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

    sidebar.draw(
        screen,
        game,
        forest_map,
        game.selected_tile
    )

    debug_menu.draw(screen, game, forest_map)

    pygame.display.flip()

pygame.quit()