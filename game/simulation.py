import random

from world.fire import FIRE_DAMAGE, FIRE_EXTINGUISH_RATE, spread_fire


def simulate_fire_day(forest_map, environment):
    burning_tiles = []
    for row in forest_map.tiles:
        for tile in row:
            if tile.ground_type == "water":
                continue
            if tile.firebreak and tile.firebreak_progress < 100:
                tile.firebreak_progress = min(100, tile.firebreak_progress + 25)
                tile.firebreak_active = tile.firebreak_progress >= 100
            if tile.fire_active:
                burning_tiles.append(tile)

    evaluated = set()
    for tile in burning_tiles:
        tile.fire_age += 1
        damage = FIRE_DAMAGE * (0.6 + tile.fire_intensity / 100.0)
        if environment.rainfall > 55:
            damage *= 0.7
        if tile.water > 40:
            damage *= 0.8

        tile.health = max(0, tile.health - damage)
        tile.biodiversity = max(0, tile.biodiversity - damage * 0.7)
        tile.water = max(0, tile.water - damage * 0.6)
        tile.fire_risk = min(100, tile.fire_risk + 5)

        if tile.fire_intensity > 0:
            tile.fire_intensity = max(0, tile.fire_intensity - FIRE_EXTINGUISH_RATE * (0.7 if environment.rainfall > 50 else 1.0))
            if environment.rainfall > 60:
                tile.fire_intensity = max(0, tile.fire_intensity - 10)

        if tile.fire_intensity <= 0:
            tile.fire_active = False
            tile.fire_state = "EXTINGUISHED"
            tile.burnt = tile.health <= 35
            continue

        if tile.fire_intensity >= 70:
            tile.fire_state = "INTENSE"
        elif tile.fire_intensity >= 35:
            tile.fire_state = "BURNING"
        else:
            tile.fire_state = "IGNITED"

        for neighbor in forest_map.get_neighbors(tile):
            if neighbor.ground_type == "water":
                continue
            key = (neighbor.x, neighbor.y)
            if key in evaluated or neighbor.fire_active:
                continue
            evaluated.add(key)
            probability = random.random()
            spread_chance = 0.0
            if tile.fire_intensity > 0:
                from world.fire import compute_spread_probability
                spread_chance = compute_spread_probability(tile, neighbor, environment.wind)
            if probability < spread_chance:
                from world.fire import ignite_tile
                ignite_tile(neighbor, intensity=max(16, int(tile.fire_intensity * 0.75)))

    for row in forest_map.tiles:
        for tile in row:
            if tile.ground_type == "water":
                continue
            if tile.fire_active:
                tile.fire_risk = min(100, tile.fire_risk + 2)
            else:
                tile.fire_risk = max(0, tile.fire_risk - 0.5)

            if tile.ground_type == "burnt":
                tile.recovery_progress = min(100, tile.recovery_progress + 2 + (tile.water / 35.0))
                tile.health = min(100, tile.health + 1.0 + tile.water * 0.02)
                tile.biodiversity = min(100, tile.biodiversity + 0.8 + tile.water * 0.015)
                if tile.recovery_progress >= 70:
                    tile.ground_type = "recovering"
                    tile.burnt = False
            elif tile.ground_type == "recovering":
                tile.recovery_progress = min(100, tile.recovery_progress + 4)
                tile.health = min(100, tile.health + 1.2)
                tile.biodiversity = min(100, tile.biodiversity + 1.0)
                if tile.recovery_progress >= 100:
                    tile.ground_type = "forest"
                    tile.burnt = False
            else:
                if tile.health < 100:
                    gain = 0.5 + (tile.water / 100.0) * 1.2
                    tile.health = min(100, tile.health + gain)
                    tile.biodiversity = min(100, tile.biodiversity + gain * 0.5)
                    tile.water = min(100, tile.water + 0.3)
                    if tile.health > 75:
                        tile.ground_type = "forest"

    return environment


def simulate_day(forest_map, environment):
    environment.apply_daily()
    simulate_fire_day(forest_map, environment)
    return environment
