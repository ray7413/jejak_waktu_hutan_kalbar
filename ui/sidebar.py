import pygame

from config import WHITE


class Sidebar:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "arial",
            20
        )

        self.big_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

    def draw(self, screen, year):

        # Left panel

        pygame.draw.rect(
            screen,
            (35, 38, 35),
            (20, 20, 230, 680),
            border_radius=10
        )

        title = self.big_font.render(
            "FOREST",
            True,
            WHITE
        )

        screen.blit(
            title,
            (45, 45)
        )

        year_text = self.font.render(
            f"Year {year}",
            True,
            WHITE
        )

        screen.blit(
            year_text,
            (45, 100)
        )