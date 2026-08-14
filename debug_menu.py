import pygame


class DebugMenu:
    def __init__(self):
        self.visible = False
        self.font = pygame.font.SysFont("arial", 16)
        self.title_font = pygame.font.SysFont("arial", 20, bold=True)
        self.buttons = {}

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, game, forest_map):
        if not self.visible:
            return

        panel = pygame.Rect(screen.get_width() - 320, 80, 300, 470)
        pygame.draw.rect(screen, (30, 34, 30), panel, border_radius=10)
        pygame.draw.rect(screen, (140, 164, 140), panel, 2, border_radius=10)

        title = self.title_font.render("DEBUG MENU", True, (255, 255, 255))
        screen.blit(title, (panel.x + 18, panel.y + 14))

        self.buttons.clear()
        y = panel.y + 52
        controls = [
            ("Pause", (panel.x + 16, y, 120, 28)),
            ("Resume", (panel.x + 146, y, 120, 28)),
            ("Advance 1d", (panel.x + 16, y + 36, 120, 28)),
            ("Advance 7d", (panel.x + 146, y + 36, 120, 28)),
            ("Advance 30d", (panel.x + 16, y + 72, 120, 28)),
            ("Dryness +", (panel.x + 146, y + 72, 120, 28)),
            ("Dryness -", (panel.x + 16, y + 108, 120, 28)),
            ("Water +", (panel.x + 146, y + 108, 120, 28)),
            ("Water -", (panel.x + 16, y + 144, 120, 28)),
            ("Ignite Tile", (panel.x + 146, y + 144, 120, 28)),
            ("Ignite Random", (panel.x + 16, y + 180, 120, 28)),
            ("Ignite Area", (panel.x + 146, y + 180, 120, 28)),
            ("Extinguish Tile", (panel.x + 16, y + 216, 120, 28)),
            ("Extinguish All", (panel.x + 146, y + 216, 120, 28)),
            ("Damage Tile", (panel.x + 16, y + 252, 120, 28)),
            ("Restore Tile", (panel.x + 146, y + 252, 120, 28)),
            ("Set Healthy", (panel.x + 16, y + 288, 120, 28)),
            ("Set Burnt", (panel.x + 146, y + 288, 120, 28)),
            ("Close", (panel.x + 16, y + 370, 120, 28)),
        ]

        for label, rect in controls:
            self.buttons[label] = pygame.Rect(*rect)
            pygame.draw.rect(screen, (65, 75, 65), rect, border_radius=6)
            text = self.font.render(label, True, (245, 245, 245))
            screen.blit(text, (rect[0] + 10, rect[1] + 6))

        info = [
            f"Date: {game.current_date}",
            f"Dryness: {game.dryness}%",
            f"Speed: {game.simulation_speed}x",
            f"Paused: {'yes' if game.paused else 'no'}",
            f"Fires: {game.active_fire_count}",
            f"Selected: {game.selected_tile}",
        ]
        iy = panel.y + 420
        for line in info:
            text = self.font.render(line, True, (220, 220, 220))
            screen.blit(text, (panel.x + 12, iy))
            iy += 18

    def handle_click(self, pos, game, forest_map):
        if not self.visible:
            return False

        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.handle_action(label, game, forest_map)
                return True
        return False

    def handle_action(self, label, game, forest_map):
        if label == "Pause":
            game.pause()
        elif label == "Resume":
            game.resume()
        elif label == "Advance 1d":
            game.advance_days(1)
        elif label == "Advance 7d":
            game.advance_days(7)
        elif label == "Advance 30d":
            game.advance_days(30)
        elif label == "Dryness +":
            game.dryness = min(100, game.dryness + 10)
        elif label == "Dryness -":
            game.dryness = max(0, game.dryness - 10)
        elif label == "Water +":
            for row in forest_map.tiles:
                for tile in row:
                    if tile.type != "water":
                        tile.water = min(100, tile.water + 15)
        elif label == "Water -":
            for row in forest_map.tiles:
                for tile in row:
                    if tile.type != "water":
                        tile.water = max(0, tile.water - 15)
        elif label == "Ignite Tile":
            game.ignite_selected_tile()
        elif label == "Ignite Random":
            game.ignite_random_tile()
        elif label == "Ignite Area":
            game.ignite_random_area()
        elif label == "Extinguish Tile":
            game.extinguish_selected_tile()
        elif label == "Extinguish All":
            game.extinguish_all_fires()
        elif label == "Damage Tile":
            game.damage_selected_tile()
        elif label == "Restore Tile":
            game.restore_selected_tile()
        elif label == "Set Healthy":
            game.set_selected_tile_healthy()
        elif label == "Set Burnt":
            game.set_selected_tile_burnt()
        elif label == "Close":
            self.visible = False
