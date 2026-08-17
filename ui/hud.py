import pygame


class HUD:
    def __init__(self):
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_medium = pygame.font.SysFont("arial", 18, bold=True)
        self.font_large = pygame.font.SysFont("arial", 22, bold=True)
        self.buttons = {}

    def draw(self, screen, game_state):
        top_bar = pygame.Rect(260, 16, max(760, screen.get_width() - 420), 68)
        pygame.draw.rect(screen, (39, 45, 42), top_bar, border_radius=10)
        date_text = self.font_medium.render(game_state.current_date.strftime("%b %d, %Y"), True, (240, 240, 240))
        screen.blit(date_text, (top_bar.x + 18, top_bar.y + 22))

        stats = game_state.forest_map.stats()
        screen.blit(self.font_small.render(f"Forest: {stats['health']}%", True, (240, 240, 240)), (top_bar.x + 220, top_bar.y + 22))
        screen.blit(self.font_small.render(f"Biodiversity: {stats['biodiversity']}%", True, (240, 240, 240)), (top_bar.x + 345, top_bar.y + 22))
        screen.blit(self.font_small.render(f"Water: {stats['water']}%", True, (240, 240, 240)), (top_bar.x + 520, top_bar.y + 22))
        screen.blit(self.font_small.render(f"Fires: {stats['fires']}", True, (255, 120, 80)), (top_bar.x + 620, top_bar.y + 22))

        controls = [
            ("PAUSE", (top_bar.x + 710, top_bar.y + 16, 78, 32)),
            ("PLAY", (top_bar.x + 794, top_bar.y + 16, 78, 32)),
            ("1x", (top_bar.x + 880, top_bar.y + 16, 48, 32)),
            ("2x", (top_bar.x + 934, top_bar.y + 16, 48, 32)),
            ("5x", (top_bar.x + 988, top_bar.y + 16, 48, 32)),
            ("MENU", (screen.get_width() - 110, 18, 90, 34)),
        ]
        self.buttons = {}
        for label, rect in controls:
            pygame.draw.rect(screen, (74, 82, 70), rect, border_radius=8)
            text = self.font_medium.render(label, True, (248, 248, 248))
            screen.blit(text, (rect[0] + 10, rect[1] + 5))
            self.buttons[label] = pygame.Rect(*rect)

        side = pygame.Rect(18, 110, 250, 620)
        pygame.draw.rect(screen, (35, 38, 36), side, border_radius=12)
        title = self.font_large.render("FOREST", True, (245, 245, 245))
        screen.blit(title, (side.x + 18, side.y + 16))

        labels = [
            f"Health: {stats['health']}%",
            f"Biodiversity: {stats['biodiversity']}%",
            f"Water: {stats['water']}%",
            f"Coverage: {stats['forest']}%",
            f"Burnt: {stats['burnt']}",
            f"Recovering: {stats['recovering']}",
        ]
        py = side.y + 70
        for label in labels:
            text = self.font_small.render(label, True, (230, 230, 230))
            screen.blit(text, (side.x + 18, py))
            py += 26

        action_names = [
            ("FIREFIGHT", "F"),
            ("FIREBREAK", "B"),
            ("REPLANT", "R"),
            ("RESTORE_WATER", "W"),
            ("PROTECT", "P"),
            ("MONITOR", "M"),
        ]
        y = side.y + 260
        for name, key in action_names:
            rect = pygame.Rect(side.x + 18, y, 210, 34)
            pygame.draw.rect(screen, (62, 70, 62), rect, border_radius=8)
            txt = self.font_small.render(f"{name} ({key}) {game_state.actions.resources[name]}", True, (245, 245, 245))
            screen.blit(txt, (rect.x + 10, rect.y + 8))
            self.buttons[name] = rect
            y += 42

        if game_state.selected_tile is not None:
            tile = game_state.forest_map.get_tile(*game_state.selected_tile)
            line_y = side.y + 500
            info = [
                f"Tile {tile.x},{tile.y}",
                f"State: {tile.get_state_label()}",
                f"Health: {tile.health}",
                f"Biodiversity: {tile.biodiversity}",
                f"Water: {tile.water}",
                f"Fire Risk: {tile.fire_risk}",
            ]
            for line in info:
                screen.blit(self.font_small.render(line, True, (240, 240, 240)), (side.x + 18, line_y))
                line_y += 22

        message = self.font_small.render(game_state.message, True, (205, 220, 205))
        screen.blit(message, (18, 760))

    def handle_click(self, pos, game_state):
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if label in {"PAUSE", "PLAY"}:
                    if label == "PAUSE":
                        game_state.time.pause()
                    else:
                        game_state.time.resume()
                elif label in {"1x", "2x", "5x"}:
                    game_state.time.set_speed(int(label[0]))
                elif label == "MENU":
                    return "MENU"
                elif label in {"FIREFIGHT", "FIREBREAK", "REPLANT", "RESTORE_WATER", "PROTECT", "MONITOR"}:
                    game_state.apply_action(label)
                return label
        return None
