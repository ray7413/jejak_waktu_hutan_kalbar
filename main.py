import pygame

pygame.init()

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND
)

from map.forest_map import ForestMap

# initialization

clock = pygame.time.Clock()
running = True

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Jejak Waktu")

forest_map = ForestMap()

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw
    screen.fill(BACKGROUND)
    forest_map.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()