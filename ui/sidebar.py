import pygame

from config import WHITE


class Sidebar:

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.big_font = pygame.font.SysFont("arial", 28, bold=True)
        self.button_rects = {}
        self.hud_buttons = {}

    def draw(self, screen, game, forest_map, selected_tile):
        # Top HUD across screen
        hud = pygame.Rect(250, 14, screen.get_width() - 270, 60)
        pygame.draw.rect(screen, (40, 45, 40), hud, border_radius=10)

        date_text = self.font.render(game.current_date.strftime("%b %d, %Y"), True, WHITE)
        screen.blit(date_text, (hud.x + 18, hud.y + 18))

        speed_text = self.font.render(f"{game.simulation_speed}x", True, WHITE)
        screen.blit(speed_text, (hud.x + 220, hud.y + 18))

        dryness_text = self.font.render(f"Dry: {game.dryness}%", True, WHITE)
        screen.blit(dryness_text, (hud.x + 290, hud.y + 18))

        fires_text = self.font.render(f"Fires: {game.active_fire_count}", True, WHITE)
        screen.blit(fires_text, (hud.x + 420, hud.y + 18))

        self.hud_buttons.clear()
        button_defs = [
            ("PAUSE", (hud.x + 530, hud.y + 14, 70, 28)),
            ("PLAY", (hud.x + 610, hud.y + 14, 70, 28)),
            ("1x", (hud.x + 690, hud.y + 14, 42, 28)),
            ("2x", (hud.x + 738, hud.y + 14, 42, 28)),
            ("5x", (hud.x + 786, hud.y + 14, 42, 28)),
            ("MENU", (screen.get_width() - 120, 14, 90, 32)),
        ]
        for label, rect in button_defs:
            button = pygame.Rect(*rect)
            self.hud_buttons[label] = button
            pygame.draw.rect(screen, (60, 72, 60), button, border_radius=8)
            text = self.font.render(label, True, WHITE)
            screen.blit(text, (button.x + 10, button.y + 4))

        # Left panel for game actions and stats
        panel = pygame.Rect(20, 20, 230, 680)
        pygame.draw.rect(screen, (35, 38, 35), panel, border_radius=10)

        title = self.big_font.render("FOREST", True, WHITE)
        screen.blit(title, (45, 45))

        stats = forest_map.get_global_stats()
        info_y = 110
        labels = [
            (f"Health: {stats['health']}%", 45, info_y),
            (f"Biodiversity: {stats['biodiversity']}%", 45, info_y + 25),
            (f"Water: {stats['water']}%", 45, info_y + 50),
            (f"Coverage: {stats['coverage']}%", 45, info_y + 75),
            (f"Burned: {stats['burned']}", 45, info_y + 100),
            (f"Recovering: {stats['recovering']}", 45, info_y + 125),
        ]
        for text, x, y in labels:
            render = self.small_font.render(text, True, WHITE)
            screen.blit(render, (x, y))

        self.button_rects = {}
        action_y = 300
        for name, key, x, y, w, h in [
            ("RESTORE", "R", 40, action_y, 170, 32),
            ("REPLANT", "P", 40, action_y + 40, 170, 32),
            ("PROTECT", "T", 40, action_y + 80, 170, 32),
        ]:
            rect = pygame.Rect(x, y, w, h)
            self.button_rects[name] = rect
            pygame.draw.rect(screen, (70, 80, 70), rect, border_radius=8)
            button_text = self.font.render(f"{name} ({key})", True, WHITE)
            screen.blit(button_text, (x + 12, y + 6))

        if selected_tile:
            x, y = selected_tile
            tile = forest_map.tiles[y][x]
            info = [
                f"Tile {x},{y}",
                f"State: {tile.get_state_label()}",
                f"Health: {tile.health}",
                f"Biodiversity: {tile.biodiversity}",
                f"Water: {tile.water}",
                f"Forest Age: {tile.forest_age}",
                f"Fire Risk: {tile.fire_risk}",
            ]
            info_y = 500
            for line in info:
                render = self.small_font.render(line, True, WHITE)
                screen.blit(render, (40, info_y))
                info_y += 20

        if selected_tile:
            tile = forest_map.tiles[selected_tile[1]][selected_tile[0]]
            if tile.fire_active:
                fire_text = self.font.render("🔥 FIRE ACTIVE", True, (255, 120, 80))
                screen.blit(fire_text, (40, 630))
                intensity_text = self.small_font.render(f"Intensity: {tile.fire_intensity}", True, WHITE)
                screen.blit(intensity_text, (40, 652))

        render = self.small_font.render(
            f"Action Points: Restore {game.resources['restore']} | Replant {game.resources['replant']} | Protect {game.resources['protect']}",
            True,
            WHITE,
        )
        screen.blit(render, (25, 690))

    def handle_click(self, pos, game):
        for name, rect in self.hud_buttons.items():
            if rect.collidepoint(pos):
                if name == "PAUSE":
                    game.pause()
                elif name == "PLAY":
                    game.resume()
                elif name == "1x":
                    game.set_speed(1)
                elif name == "2x":
                    game.set_speed(2)
                elif name == "5x":
                    game.set_speed(5)
                elif name == "MENU":
                    return "MENU"
                return name

        for name, rect in self.button_rects.items():
            if rect.collidepoint(pos):
                if name == "RESTORE":
                    game.apply_restore()
                elif name == "REPLANT":
                    game.apply_replant()
                elif name == "PROTECT":
                    game.apply_protect()
                return name
        return None
