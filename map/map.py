import pygame
import random

from .tiles import Tile

from config import (
    MAP_WIDTH,
    MAP_HEIGHT,
    MAP_OFFSET_X,
    MAP_OFFSET_Y,
    MAP_ZOOM_MIN,
    MAP_ZOOM_MAX
)

class ForestMap:

    def __init__(self):

        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.offset_x = MAP_OFFSET_X
        self.offset_y = MAP_OFFSET_Y

        self.zoom = 1
        self.min_zoom = MAP_ZOOM_MIN
        self.min_zoom = MAP_ZOOM_MAX

        self.tiles = []

        self.gener
