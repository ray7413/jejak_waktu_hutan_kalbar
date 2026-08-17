import random

FIRE_BASE_SPREAD_CHANCE = 0.12
FIRE_DRYNESS_MULTIPLIER = 0.016
FIRE_WATER_MULTIPLIER = 0.012
FIRE_FUEL_MULTIPLIER = 0.7
FIRE_WIND_MULTIPLIER = 1.5
FIREBREAK_MULTIPLIER = 0.2
FIRE_DAMAGE = 1.8
FIRE_MAX_INTENSITY = 100
FIRE_EXTINGUISH_RATE = 4
FIRE_NEW_FIRE_MULTIPLIER = 0.5
FIRE_INTENSE_MULTIPLIER = 1.4
FIRE_NORMAL_FIRE_MULTIPLIER = 1.0

WIND_MULTIPLIERS = {
    "N": {"N": 1.4, "S": 0.5, "E": 1.0, "W": 1.0, "NE": 1.2, "NW": 1.2, "SE": 0.7, "SW": 0.7},
    "NE": {"NE": 1.4, "SW": 0.5, "E": 1.2, "N": 1.2, "W": 0.8, "S": 0.8, "NW": 0.8, "SE": 1.0},
    "E": {"E": 1.5, "W": 0.5, "N": 1.0, "S": 1.0, "NE": 1.2, "SE": 1.2, "NW": 0.8, "SW": 0.8},
    "SE": {"SE": 1.4, "NW": 0.5, "E": 1.2, "S": 1.2, "N": 0.8, "W": 0.8, "NE": 1.0, "SW": 1.0},
    "S": {"S": 1.4, "N": 0.5, "E": 1.0, "W": 1.0, "SE": 1.2, "SW": 1.2, "NE": 0.7, "NW": 0.7},
    "SW": {"SW": 1.4, "NE": 0.5, "W": 1.2, "S": 1.2, "N": 0.8, "E": 0.8, "NW": 1.0, "SE": 1.0},
    "W": {"W": 1.5, "E": 0.5, "N": 1.0, "S": 1.0, "NW": 1.2, "SW": 1.2, "NE": 0.8, "SE": 0.8},
    "NW": {"NW": 1.4, "SE": 0.5, "W": 1.2, "N": 1.2, "E": 0.8, "S": 0.8, "NE": 1.0, "SW": 1.0},
}


def _fire_stage_multiplier(tile):
    intensity = tile.fire_intensity
    if intensity < 20:
        return FIRE_NEW_FIRE_MULTIPLIER
    if intensity < 60:
        return FIRE_NORMAL_FIRE_MULTIPLIER
    if intensity < 90:
        return FIRE_INTENSE_MULTIPLIER
    return 1.2


def _relative_wind_direction(source_tile, target_tile):
    dx = target_tile.x - source_tile.x
    dy = target_tile.y - source_tile.y

    if dx == 0 and dy < 0:
        return "N"
    if dx > 0 and dy < 0:
        return "NE"
    if dx > 0 and dy == 0:
        return "E"
    if dx > 0 and dy > 0:
        return "SE"
    if dx == 0 and dy > 0:
        return "S"
    if dx < 0 and dy > 0:
        return "SW"
    if dx < 0 and dy == 0:
        return "W"
    if dx < 0 and dy < 0:
        return "NW"
    return "E"


def compute_spread_probability(source_tile, target_tile, wind_direction="E"):
    if target_tile.ground_type == "water" or target_tile.fire_active:
        return 0.0

    dryness = max(0, min(100, getattr(target_tile, "dryness", 50)))
    water_penalty = max(0, 100 - target_tile.water) / 100.0
    fuel_value = 0.6 + (target_tile.biodiversity / 100.0) * 0.9 + (target_tile.health / 100.0) * 0.5
    base = FIRE_BASE_SPREAD_CHANCE
    if dryness > 70:
        base = max(base, FIRE_BASE_SPREAD_CHANCE * 1.8)
    elif dryness < 25:
        base *= 0.6

    wind_rel = _relative_wind_direction(source_tile, target_tile)
    wind_multiplier = WIND_MULTIPLIERS.get(wind_direction, {}).get(wind_rel, 1.0)

    firebreak_factor = FIREBREAK_MULTIPLIER if target_tile.firebreak and getattr(target_tile, "firebreak_progress", 100) >= 40 else 1.0
    protected_factor = 0.7 if target_tile.protected else 1.0
    stage_multiplier = _fire_stage_multiplier(source_tile)

    chance = base * (1.0 + (dryness * FIRE_DRYNESS_MULTIPLIER)) * (1.0 - (target_tile.water * FIRE_WATER_MULTIPLIER))
    chance *= fuel_value * FIRE_FUEL_MULTIPLIER
    chance *= stage_multiplier
    chance *= wind_multiplier
    chance *= firebreak_factor
    chance *= protected_factor
    chance = max(0.0, min(1.0, chance * (1.0 - water_penalty * 0.25)))
    return chance


def ignite_tile(tile, intensity=45):
    if tile.ground_type == "water":
        return False
    tile.fire_active = True
    tile.fire_intensity = max(12, min(FIRE_MAX_INTENSITY, intensity))
    tile.fire_age = 0
    tile.fire_state = "IGNITED"
    tile.health = max(0, tile.health - 8)
    tile.biodiversity = max(0, tile.biodiversity - 6)
    return True


def extinguish_tile(tile):
    tile.fire_active = False
    tile.fire_intensity = 0
    tile.fire_age = 0
    tile.fire_state = "EXTINGUISHED"
    if tile.health <= 35:
        tile.ground_type = "burnt"
    tile.burnt = tile.health <= 35
    return True


def spread_fire(forest_map, tile, wind_direction="E"):
    if not tile.fire_active or tile.ground_type == "water":
        return

    evaluated = set()
    for neighbor in forest_map.get_neighbors(tile):
        if neighbor.ground_type == "water" or neighbor.fire_active:
            continue

        key = (neighbor.x, neighbor.y)
        if key in evaluated:
            continue
        evaluated.add(key)

        chance = compute_spread_probability(tile, neighbor, wind_direction)
        if random.random() < chance:
            ignite_tile(neighbor, intensity=max(18, int(tile.fire_intensity * 0.7)))

    tile.fire_age += 1
    tile.fire_intensity = max(0, tile.fire_intensity - FIRE_EXTINGUISH_RATE * 0.4)

    if tile.fire_intensity <= 5:
        tile.fire_active = False
        tile.fire_state = "WEAKENING"
        tile.burnt = True
