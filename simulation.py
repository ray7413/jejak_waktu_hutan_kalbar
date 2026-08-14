import random

from fire import process_fire_dynamics


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def simulate_day(forest_map, game_state):
    if not forest_map or not game_state:
        return

    weather_delta = 0
    if game_state.dryness > 60:
        weather_delta += 1
    if game_state.dryness < 30:
        weather_delta -= 1

    game_state.dryness = clamp(game_state.dryness + weather_delta + random.randint(-3, 3))

    for row in forest_map.tiles:
        for tile in row:
            if tile.type == "water":
                continue

            tile.fire_risk = clamp(tile.fire_risk + (game_state.dryness - 50) * 0.08)
            tile.water = clamp(tile.water - (game_state.dryness / 100.0) * 4)

            if tile.fire_active:
                tile.fire_age += 1

            if tile.fire_active and tile.fire_intensity <= 0:
                tile.fire_active = False
                tile.burned = True
                tile.recovering = True

    process_fire_dynamics(forest_map, game_state)

    for row in forest_map.tiles:
        for tile in row:
            if tile.type == "water":
                continue

            if tile.fire_active:
                tile.health = max(0, tile.health - (tile.fire_intensity / 100.0) * 7)
                tile.biodiversity = max(0, tile.biodiversity - (tile.fire_intensity / 100.0) * 6)
                tile.degradation = min(100, tile.degradation + 5)
                tile.burned = tile.fire_active or tile.health < 25
            else:
                if tile.health < 100:
                    tile.health = min(100, tile.health + 0.8 + (tile.water / 200.0))
                    tile.biodiversity = min(100, tile.biodiversity + 0.4 + (tile.water / 250.0))
                    tile.degradation = max(0, tile.degradation - 1)

                if tile.burned and tile.health > 35:
                    tile.burned = False
                    tile.recovering = True

            if tile.fire_active:
                tile.recovering = True
            elif tile.health > 70 and tile.degradation < 20:
                tile.recovering = False

            tile.update_visual_state()

    forest_map.refresh_tile_states()
    forest_map.get_global_stats()
    return game_state.current_date
