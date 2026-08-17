import os
import pygame


class AssetManager:
    def __init__(self, base_dir="assets"):
        self.base_dir = base_dir
        self.ground = {}
        self.vegetation = {}
        self.effects = {}
        self.ui = {}
        self._load()

    def _load_surface(self, relative_path, fallback_color=(80, 120, 80), fallback_size=(80, 40)):
        if not relative_path:
            surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
            surface.fill(fallback_color)
            return surface

        path = os.path.join(self.base_dir, relative_path)
        if os.path.isfile(path):
            image = pygame.image.load(path).convert_alpha()
            if image.get_width() > 0 and image.get_height() > 0:
                return image

        surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surface.fill(fallback_color)
        return surface

    def _load(self):
        ground_files = {
            "forest": ["ground/forest.png"],
            "recovering": ["ground/recovering.png"],
            "degraded": ["ground/degraded.png"],
            "burnt": ["ground/burnt.png", "ground/degraded.png"],
            "water": ["ground/water.png"],
        }
        for key, candidates in ground_files.items():
            for candidate in candidates:
                if os.path.exists(os.path.join(self.base_dir, candidate)):
                    self.ground[key] = self._load_surface(candidate)
                    break
            else:
                self.ground[key] = self._load_surface("", fallback_color=(70, 100, 70), fallback_size=(80, 40))

        vegetation_files = {
            "tree_standard": ["trees/tree_small.png", "trees/palm.png"],
            "tree_palm": ["trees/palm.png", "trees/tree_small.png"],
            "grass": ["vegetation/grass.png", "trees/tree_small.png"],
            "bush": ["vegetation/bush.png", "trees/tree_small.png"],
            "burnt": ["trees/burnt_1.png", "trees/burnt_2.png"],
            "none": ["trees/tree_small.png"],
        }
        for key, candidates in vegetation_files.items():
            for candidate in candidates:
                if os.path.exists(os.path.join(self.base_dir, candidate)):
                    self.vegetation[key] = self._load_surface(candidate)
                    break
            else:
                self.vegetation[key] = self._load_surface("", fallback_color=(90, 140, 90), fallback_size=(60, 60))

        fire_path = os.path.join(self.base_dir, "disasters/fire.png")
        smoke_path = os.path.join(self.base_dir, "disasters/smoke.png")
        self.effects["fire"] = self._load_surface("disasters/fire.png", fallback_color=(220, 110, 40), fallback_size=(40, 40)) if os.path.exists(fire_path) else self._load_surface("", fallback_color=(220, 110, 40), fallback_size=(40, 40))
        self.effects["smoke"] = self._load_surface("disasters/smoke.png", fallback_color=(140, 140, 140), fallback_size=(40, 40)) if os.path.exists(smoke_path) else self._load_surface("", fallback_color=(140, 140, 140), fallback_size=(40, 40))

        selection_path = os.path.join(self.base_dir, "ui/selection_tile.png")
        hover_path = os.path.join(self.base_dir, "ui/hover_tile.png")
        self.ui["selection"] = self._load_surface("ui/selection_tile.png", fallback_color=(90, 210, 100), fallback_size=(80, 40)) if os.path.exists(selection_path) else self._load_surface("", fallback_color=(90, 210, 100), fallback_size=(80, 40))
        self.ui["hover"] = self._load_surface("ui/hover_tile.png", fallback_color=(150, 160, 190), fallback_size=(80, 40)) if os.path.exists(hover_path) else self._load_surface("", fallback_color=(150, 160, 190), fallback_size=(80, 40))

    def ground_for(self, ground_type):
        return self.ground.get(ground_type, self.ground["forest"])

    def vegetation_for(self, vegetation_type):
        return self.vegetation.get(vegetation_type, self.vegetation["tree_standard"])

    def effect_for(self, key):
        return self.effects.get(key, self.effects["fire"])

    def ui_for(self, key):
        return self.ui.get(key, self.ui["selection"])
