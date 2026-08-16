import os

import pygame

ASSET_ROOT = os.path.dirname(__file__)

# ground tiles
forest = pygame.image.load(os.path.join(ASSET_ROOT, "ground", "forest.png"))
burnt = pygame.image.load(os.path.join(ASSET_ROOT, "ground", "burnt.png"))
degraded = pygame.image.load(os.path.join(ASSET_ROOT, "ground", "degraded.png"))
recovering = pygame.image.load(os.path.join(ASSET_ROOT, "ground", "recovering.png"))
water = pygame.image.load(os.path.join(ASSET_ROOT, "ground", "water.png"))

# select asset
select = pygame.image.load(os.path.join(ASSET_ROOT, "select.png"))
