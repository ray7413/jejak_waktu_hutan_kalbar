import random

import pygame


class DebugMenu:
    def __init__(self):
        self.visible = False
        self.font = pygame.font.SysFont("arial", 16)
        self.title_font = pygame.font.SysFont("arial", 20, bold=True)
        self.buttons = {}

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, game_state):
        if not self.visible:
            return
        panel = pygame.Rect(screen.get_width() - 330, 80, 310, 540)
        pygame.draw.rect(screen, (30, 34, 30), panel, border_radius=10)
        pygame.draw.rect(screen, (140, 164, 140), panel, 2, border_radius=10)
        screen.blit(self.title_font.render("DEBUG MENU", True, (255, 255, 255)), (panel.x + 18, panel.y + 14))

        controls = [
            ("ADV 1 DAY", (panel.x + 16, panel.y + 52, 118, 28)),
            ("IGNITE SELECTED", (panel.x + 146, panel.y + 52, 118, 28)),
            ("IGNITE RANDOM", (panel.x + 16, panel.y + 92, 118, 28)),
            ("IGNITE RANDOM AREA", (panel.x + 146, panel.y + 92, 118, 28)),
            ("EXTINGUISH SELECTED", (panel.x + 16, panel.y + 132, 118, 28)),
            ("EXTINGUISH ALL", (panel.x + 146, panel.y + 132, 118, 28)),
            ("DRY +10", (panel.x + 16, panel.y + 172, 118, 28)),
            ("DRY -10", (panel.x + 146, panel.y + 172, 118, 28)),
            ("WIND ->", (panel.x + 16, panel.y + 212, 118, 28)),
            ("WIND <-", (panel.x + 146, panel.y + 212, 118, 28)),
            ("WIND ↑", (panel.x + 16, panel.y + 252, 118, 28)),
            ("WIND ↓", (panel.x + 146, panel.y + 252, 118, 28)),
            ("LOW INT", (panel.x + 16, panel.y + 292, 118, 28)),
            ("HIGH INT", (panel.x + 146, panel.y + 292, 118, 28)),
            ("CLOSE", (panel.x + 70, panel.y + 340, 150, 36)),
        ]
        self.buttons = {}
        for label, rect in controls:
            self.buttons[label] = pygame.Rect(*rect)
            pygame.draw.rect(screen, (66, 76, 66), rect, border_radius=6)
            screen.blit(self.font.render(label, True, (245, 245, 245)), (rect[0] + 8, rect[1] + 6))

        info = [
            f"Date: {game_state.current_date}",
            f"Dryness: {game_state.environment.dryness}%",
            f"Wind: {game_state.environment.wind}",
            f"Speed: {game_state.time.speed}x",
            f"Paused: {'yes' if game_state.time.paused else 'no'}",
            f"Fires: {game_state.forest_map.stats()['fires']}",
        ]
        y = panel.y + 395
        for line in info:
            screen.blit(self.font.render(line, True, (220, 220, 220)), (panel.x + 18, y))
            y += 20

    def handle_click(self, pos, game_state):
        if not self.visible:
            return False
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if label == "ADV 1 DAY":
                    game_state.advance_day()
                elif label == "IGNITE SELECTED":
                    game_state.ignite_selected()
                elif label == "IGNITE RANDOM":
                    rows = game_state.forest_map.tiles
                    row = rows[random.randrange(len(rows))]
                    cell = row[random.randrange(len(row))]
                    from world.fire import ignite_tile
                    ignite_tile(cell, intensity=random.randint(30, 70))
                elif label == "IGNITE RANDOM AREA":
                    rows = game_state.forest_map.tiles
                    cx = random.randrange(len(rows[0]))
                    cy = random.randrange(len(rows))
                    for y in range(max(0, cy - 1), min(len(rows), cy + 2)):
                        for x in range(max(0, cx - 1), min(len(rows[0]), cx + 2)):
                            tile = rows[y][x]
                            if tile.ground_type != "water":
                                from world.fire import ignite_tile
                                ignite_tile(tile, intensity=random.randint(20, 60))
                elif label == "EXTINGUISH SELECTED":
                    game_state.extinguish_selected()
                elif label == "EXTINGUISH ALL":
                    for row in game_state.forest_map.tiles:
                        for tile in row:
                            if tile.fire_active:
                                from world.fire import extinguish_tile
                                extinguish_tile(tile)
                elif label == "DRY +10":
                    game_state.environment.increase_dryness(10)
                elif label == "DRY -10":
                    game_state.environment.decrease_dryness(10)
                elif label == "WIND ->":
                    game_state.environment.rotate_wind(1)
                elif label == "WIND <-":
                    game_state.environment.rotate_wind(-1)
                elif label == "WIND ↑":
                    game_state.environment.set_wind("N")
                elif label == "WIND ↓":
                    game_state.environment.set_wind("S")
                elif label == "LOW INT":
                    tile = game_state.get_selected_tile()
                    if tile is not None:
                        tile.fire_intensity = 20
                        tile.fire_active = True
                elif label == "HIGH INT":
                    tile = game_state.get_selected_tile()
                    if tile is not None:
                        tile.fire_intensity = 80
                        tile.fire_active = True
                elif label == "CLOSE":
                    self.visible = False
                return True
        return False
