import pygame


class DialogueBox:
    def __init__(self):
        self.font_title = pygame.font.SysFont("arial", 24, bold=True)
        self.font_body = pygame.font.SysFont("arial", 18)
        self.font_button = pygame.font.SysFont("arial", 18, bold=True)
        self.visible = False
        self.title = "Chapter"
        self.body = ""
        self.button_text = "CONTINUE"
        self.button_rect = pygame.Rect(0, 0, 180, 44)

    def show(self, title, body):
        self.title = title
        self.body = body
        self.visible = True

    def draw(self, screen):
        if not self.visible:
            return
        panel = pygame.Rect(220, 160, screen.get_width() - 440, 420)
        pygame.draw.rect(screen, (26, 30, 28), panel, border_radius=12)
        pygame.draw.rect(screen, (142, 170, 132), panel, 2, border_radius=12)

        t = self.font_title.render(self.title, True, (245, 245, 245))
        screen.blit(t, (panel.x + 26, panel.y + 24))

        wrapped = []
        words = self.body.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if self.font_body.size(candidate)[0] > panel.width - 80:
                wrapped.append(line)
                line = word
            else:
                line = candidate
        if line:
            wrapped.append(line)

        y = panel.y + 78
        for paragraph in wrapped:
            text = self.font_body.render(paragraph, True, (230, 230, 230))
            screen.blit(text, (panel.x + 26, y))
            y += 28

        self.button_rect = pygame.Rect(panel.x + panel.width // 2 - 95, panel.y + panel.height - 84, 190, 44)
        pygame.draw.rect(screen, (88, 106, 88), self.button_rect, border_radius=10)
        btn = self.font_button.render(self.button_text, True, (245, 245, 245))
        screen.blit(btn, (self.button_rect.x + 35, self.button_rect.y + 10))

    def handle_click(self, pos):
        if self.visible and self.button_rect.collidepoint(pos):
            self.visible = False
            return True
        return False
