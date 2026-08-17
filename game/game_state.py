from datetime import date

from game.actions import ActionManager
from game.story import StoryManager
from game.time_system import TimeSystem
from world.environment import Environment


class GameState:
    def __init__(self, forest_map):
        self.forest_map = forest_map
        self.time = TimeSystem()
        self.environment = Environment()
        self.story = StoryManager()
        self.actions = ActionManager()
        self.state = "MAIN_MENU"
        self.selected_tile = None
        self.hover_tile = None
        self.message = "Forest manager ready."
        self.chapter_complete = False
        self.tutorial_step = 0
        self.final_score = 0
        self.current_date = date(1990, 1, 1)

    def get_selected_tile(self):
        if self.selected_tile is None:
            return None
        x, y = self.selected_tile
        return self.forest_map.get_tile(x, y)

    def set_state(self, state):
        self.state = state

    def advance_day(self):
        from game.simulation import simulate_day

        self.time.advance_one_day()
        self.current_date = self.time.current_date
        simulate_day(self.forest_map, self.environment)
        self.message = f"Day advanced to {self.current_date}"

    def apply_action(self, action_name, tile=None):
        tile = tile or self.get_selected_tile()
        if tile is None:
            return False
        if action_name == "FIREFIGHT":
            if not tile.fire_active:
                return False
            if not self.actions.spend("FIREFIGHT"):
                return False
            tile.fire_intensity = max(0, tile.fire_intensity - 25)
            tile.fire_risk = max(0, tile.fire_risk - 15)
            if tile.fire_intensity <= 0:
                tile.fire_active = False
                tile.fire_state = "NORMAL"
            self.message = "Firefighting suppressed the fire."
            return True
        if action_name == "FIREBREAK":
            if not self.actions.spend("FIREBREAK"):
                return False
            tile.firebreak = True
            tile.firebreak_progress = max(tile.firebreak_progress, 35)
            tile.firebreak_active = tile.firebreak_progress >= 100
            self.message = "Firebreak construction started."
            return True
        if action_name == "REPLANT":
            if not self.actions.spend("REPLANT"):
                return False
            tile.replant()
            self.message = "Replanting restored resilience."
            return True
        if action_name == "RESTORE_WATER":
            if not self.actions.spend("RESTORE_WATER"):
                return False
            tile.restore_water()
            self.message = "Water restoration improved conditions."
            return True
        if action_name == "PROTECT":
            if not self.actions.spend("PROTECT"):
                return False
            tile.protect()
            self.message = "Protection status applied."
            return True
        if action_name == "MONITOR":
            if not self.actions.spend("MONITOR"):
                return False
            tile.monitor()
            self.message = "Monitoring improved early detection."
            return True
        return False

    def ignite_selected(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        from world.fire import ignite_tile

        return ignite_tile(tile, intensity=60)

    def extinguish_selected(self):
        tile = self.get_selected_tile()
        if tile is None:
            return False
        from world.fire import extinguish_tile

        return extinguish_tile(tile)

    def summary(self):
        stats = self.forest_map.stats()
        return {
            "date": self.current_date,
            "speed": self.time.speed,
            "paused": self.time.paused,
            "health": stats["health"],
            "biodiversity": stats["biodiversity"],
            "water": stats["water"],
            "fires": stats["fires"],
            "forest_cover": stats["forest"],
            "actions": self.actions.resources,
            "message": self.message,
        }
