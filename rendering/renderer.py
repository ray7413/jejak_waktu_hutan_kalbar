import pygame


class Renderer:
    def __init__(self, asset_manager):
        self.assets = asset_manager

    def draw(self, screen, forest_map, camera, selected=None, hover=None):
        draw_tiles = []
        for row in forest_map.tiles:
            for tile in row:
                x, y = tile.x, tile.y
                sx, sy = camera.world_to_screen(x, y)
                draw_tiles.append((x + y, tile, sx, sy))

        for _, tile, sx, sy in sorted(draw_tiles, key=lambda item: item[0]):
            base = self.assets.ground_for(tile.ground_type)
            vegetation = self.assets.vegetation_for(tile.vegetation_type)
            if tile.fire_active:
                overlay = self.assets.effect_for("fire")
            else:
                overlay = None

            ground = pygame.transform.smoothscale(base, (80, 40))
            veg = pygame.transform.smoothscale(vegetation, (34, 34))

            scaled_ground = pygame.transform.smoothscale(ground, (int(80 * camera.zoom), int(40 * camera.zoom)))
            scaled_veg = pygame.transform.smoothscale(veg, (int(34 * camera.zoom), int(34 * camera.zoom)))
            draw_x = int(sx - scaled_ground.get_width() / 2)
            draw_y = int(sy - scaled_ground.get_height() / 2)
            screen.blit(scaled_ground, (draw_x, draw_y))

            if tile.vegetation_type not in {"none", "grass"}:
                screen.blit(scaled_veg, (int(sx - scaled_veg.get_width() / 2), int(sy - scaled_veg.get_height() / 2 - 10 * camera.zoom)))

            if overlay is not None:
                fire_surface = pygame.transform.smoothscale(overlay, (int(30 * camera.zoom), int(30 * camera.zoom)))
                screen.blit(fire_surface, (int(sx - fire_surface.get_width() / 2), int(sy - fire_surface.get_height() / 2)))

            if hover is not None and hover.x == tile.x and hover.y == tile.y:
                points = [
                    (sx, sy - 20 * camera.zoom),
                    (sx + 40 * camera.zoom, sy),
                    (sx, sy + 20 * camera.zoom),
                    (sx - 40 * camera.zoom, sy),
                ]
                pygame.draw.polygon(screen, (200, 210, 230), points, 2)
            if selected is not None and selected.x == tile.x and selected.y == tile.y:
                points = [
                    (sx, sy - 20 * camera.zoom),
                    (sx + 40 * camera.zoom, sy),
                    (sx, sy + 20 * camera.zoom),
                    (sx - 40 * camera.zoom, sy),
                ]
                pygame.draw.polygon(screen, (255, 255, 255), points, 2)
