import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND
)


# initialization

pygame.init()

clock = pygame.time.Clock()
running = True

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption(
    "Jejak Waktu"
)

clock = pygame.time.Clock()

while running:

    # events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # draw
    screen.fill(BACKGROUND)

    pygame.display.flip()

    clock.tick(60)


pygame.quit()