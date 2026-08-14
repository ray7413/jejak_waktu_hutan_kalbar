# Window
import pygame

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
FPS = 60

# Isometric tile
TILE_WIDTH = 80
TILE_HEIGHT = 40

# Map
MAP_WIDTH = 50
MAP_HEIGHT = 50

# Map position
MAP_OFFSET_X = 640
MAP_OFFSET_Y = 100

# Colors
BACKGROUND = (24, 27, 24)

FOREST = None
RECOVERING = None
DEGRADED = None
WATER = None

GRID = (40, 70, 42)
WHITE = (235, 235, 235)

def load_assets():
    global FOREST, RECOVERING, DEGRADED, WATER

    FOREST = pygame.image.load("assets/ground/forest.png").convert_alpha()
    RECOVERING = pygame.image.load("assets/ground/recovering.png").convert_alpha()
    DEGRADED = pygame.image.load("assets/ground/degraded.png").convert_alpha()
    WATER = pygame.image.load("assets/ground/water.png").convert_alpha()