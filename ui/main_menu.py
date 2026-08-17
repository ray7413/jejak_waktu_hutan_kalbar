import pygame


class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont("arial", 42, bold=True)
        self.font_sub = pygame.font.SysFont("arial", 22)
        self.font_button = pygame.font.SysFont("arial", 20, bold=True)
        self.buttons = {}

    def draw(self, screen):
        screen.fill((12, 18, 15))
        title = self.font_title.render("JEJAK WAKTU", True, (235, 235, 235))
        sub = self.font_title.render("HUTAN KALBAR", True, (130, 180, 120))
        subtitle = self.font_sub.render("A Forest Story", True, (220, 220, 220))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 180))
        screen.blit(sub, (screen.get_width() // 2 - sub.get_width() // 2, 235))
        screen.blit(subtitle, (screen.get_width() // 2 - subtitle.get_width() // 2, 300))

        button_rects = [
            ("START", (screen.get_width() // 2 - 110, 390, 220, 52)),
            ("QUIT", (screen.get_width() // 2 - 110, 470, 220, 52)),
        ]
        self.buttons = {}
        for label, rect in button_rects:
            pygame.draw.rect(screen, (58, 72, 58), rect, border_radius=10)
            pygame.draw.rect(screen, (132, 164, 132), rect, 2, border_radius=10)
            text = self.font_button.render(label, True, (245, 245, 245))
            screen.blit(text, (rect[0] + 70, rect[1] + 12))
            self.buttons[label] = pygame.Rect(*rect)

    def handle_click(self, pos):
        for label, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return label
        return None
