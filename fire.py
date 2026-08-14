import random


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def ignite_tile(tile, intensity=45):
    if getattr(tile, "type", None) == "water":
        return False

    tile.fire_active = True
    tile.fire_intensity = clamp(intensity)
    tile.fire_age = 0
    tile.fire_fuel = max(15, tile.biodiversity * 0.6)
    tile.fire_state = "ignited"
    tile.burned = False
    tile.recovering = True
    tile.health = max(0, tile.health - 8)
    tile.biodiversity = max(0, tile.biodiversity - 6)
    return True


def extinguish_tile(tile):
    tile.fire_active = False
    tile.fire_intensity = 0
    tile.fire_age = 0
    tile.fire_fuel = 0
    tile.fire_state = "extinguished"
    tile.burned = tile.health <= 35
    return True


def spread_fire(forest_map, tile, dryness):
    if not tile.fire_active or tile.type == "water":
        return

    for y in range(max(0, tile.y - 1), min(forest_map.height, tile.y + 2)):
        for x in range(max(0, tile.x - 1), min(forest_map.width, tile.x + 2)):
            if x == tile.x and y == tile.y:
                continue

            neighbor = forest_map.tiles[y][x]
            if neighbor.type == "water" or neighbor.fire_active:
                continue
            if neighbor.fire_intensity > 0:
                continue

            fuel = 0.6 + (neighbor.biodiversity / 100) * 0.8 + (neighbor.health / 100) * 0.5
            water_penalty = 1.0 - (neighbor.water / 100.0)
            dryness_factor = dryness / 100.0
            chance = 0.03 + (tile.fire_intensity / 100.0) * 0.22 + fuel * 0.20 + dryness_factor * 0.25 + water_penalty * 0.20

            if random.random() < chance:
                ignite_tile(neighbor, intensity=max(15, int(tile.fire_intensity * 0.65)))


def process_fire_dynamics(forest_map, game_state):
    active_fire_count = 0
    for y in range(forest_map.height):
        for x in range(forest_map.width):
            tile = forest_map.tiles[y][x]
            tile.x = x
            tile.y = y

            if tile.fire_active:
                active_fire_count += 1
                tile.fire_age += 1
                tile.fire_intensity = clamp(tile.fire_intensity - 3 - (tile.water / 100.0) * 2)

                tile.health = max(0, tile.health - (tile.fire_intensity / 100.0) * 12)
                tile.biodiversity = max(0, tile.biodiversity - (tile.fire_intensity / 100.0) * 9)
                tile.water = max(0, tile.water - (tile.fire_intensity / 100.0) * 8)
                tile.degradation = min(100, tile.degradation + 10)
                tile.fire_fuel = max(0, tile.fire_fuel - 1)

                if tile.fire_intensity <= 10:
                    tile.fire_active = False
                    tile.fire_state = "burned"
                    tile.burned = True
                    tile.recovering = True
                    tile.fire_intensity = 0
                    tile.fire_age = 0
                else:
                    tile.fire_state = "burning"

                if tile.burned:
                    tile.recovering = True

    for y in range(forest_map.height):
        for x in range(forest_map.width):
            tile = forest_map.tiles[y][x]
            if tile.fire_active:
                spread_fire(forest_map, tile, game_state.dryness)

    game_state.active_fire_count = active_fire_count
    return active_fire_count
