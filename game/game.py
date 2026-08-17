import pygame

from game.game_state import GameState
from rendering.assets import AssetManager
from rendering.camera import Camera
from rendering.renderer import Renderer
from ui.debug_menu import DebugMenu
from ui.dialogue import DialogueBox
from ui.hud import HUD
from ui.main_menu import MainMenu
from world.forest_map import ForestMap


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Jejak Waktu Hutan Kalbar")
        self.clock = pygame.time.Clock()

        self.asset_manager = AssetManager("assets")
        self.camera = Camera(x=500, y=140, zoom=1.0)
        self.forest_map = ForestMap()
        self.game_state = GameState(self.forest_map)
        self.renderer = Renderer(self.asset_manager)
        self.main_menu = MainMenu()
        self.hud = HUD()
        self.dialogue = DialogueBox()
        self.debug_menu = DebugMenu()
        self.dragging = False
        self.drag_start = None
        self.drag_origin = (0, 0)
        self.last_selected = None

    def start_game(self):
        self.game_state.set_state("PLAYING")
        self.dialogue.show("Prologue", "You manage the forest directly. Click a tile to inspect it, then respond to fire before it spreads.")
        self.game_state.message = "Click a tile to inspect the ecosystem."

    def update(self, dt):
        if self.game_state.state == "PLAYING":
            if not self.game_state.time.paused and self.game_state.time.speed > 0:
                self.game_state.time.accumulator += dt * self.game_state.time.speed
                while self.game_state.time.accumulator >= 1.0:
                    self.game_state.advance_day()
                    self.game_state.time.accumulator -= 1.0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.debug_menu.visible:
                        self.debug_menu.visible = False
                    elif self.game_state.state != "MAIN_MENU":
                        self.game_state.state = "PLAYING"
                elif event.key == pygame.K_SPACE:
                    if self.game_state.time.paused:
                        self.game_state.time.resume()
                    else:
                        self.game_state.time.pause()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.game_state.state == "MAIN_MENU":
                    result = self.main_menu.handle_click(pos)
                    if result == "START":
                        self.start_game()
                    elif result == "QUIT":
                        return "QUIT"
                    continue

                if self.dialogue.visible:
                    if self.dialogue.handle_click(pos):
                        self.game_state.state = "PLAYING"
                    continue

                if self.debug_menu.visible and self.debug_menu.handle_click(pos, self.game_state):
                    continue

                hud_click = self.hud.handle_click(pos, self.game_state)
                if hud_click is not None:
                    if hud_click == "MENU":
                        self.debug_menu.toggle()
                    continue

                if event.button in (2, 3):
                    self.dragging = True
                    self.drag_start = pos
                    self.drag_origin = (self.camera.x, self.camera.y)
                    continue

                if event.button == 1:
                    clicked_tile = self.forest_map.get_tile_at_screen(pos[0], pos[1], self.camera)
                    if clicked_tile is not None:
                        self.game_state.selected_tile = (clicked_tile.x, clicked_tile.y)
                        self.game_state.message = f"Selected tile {clicked_tile.x},{clicked_tile.y}."
                        self.last_selected = clicked_tile
                    else:
                        self.game_state.selected_tile = None
                    continue

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (2, 3):
                    self.dragging = False
                    self.drag_start = None

            if event.type == pygame.MOUSEMOTION:
                if self.dragging and self.drag_start is not None:
                    dx = event.pos[0] - self.drag_start[0]
                    dy = event.pos[1] - self.drag_start[1]
                    self.camera.x = self.drag_origin[0] - dx
                    self.camera.y = self.drag_origin[1] - dy
                    continue

                x, y = event.pos
                hovered = self.forest_map.get_tile_at_screen(x, y, self.camera)
                self.game_state.hover_tile = None if hovered is None else (hovered.x, hovered.y)

            if event.type == pygame.MOUSEWHEEL:
                if self.game_state.state != "MAIN_MENU":
                    self.camera.zoom = max(0.7, min(1.8, self.camera.zoom + event.y * 0.1))
        return None

    def render(self):
        self.screen.fill((12, 18, 15))
        if self.game_state.state == "MAIN_MENU":
            self.main_menu.draw(self.screen)
            pygame.display.flip()
            return

        self.renderer.draw(self.screen, self.forest_map, self.camera, selected=self.game_state.get_selected_tile(), hover=None)
        self.hud.draw(self.screen, self.game_state)
        if self.debug_menu.visible:
            self.debug_menu.draw(self.screen, self.game_state)
        if self.dialogue.visible:
            self.dialogue.draw(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            result = self.handle_events()
            if result == "QUIT":
                break
            self.update(dt)
            self.render()
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
