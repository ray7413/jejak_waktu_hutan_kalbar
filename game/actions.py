class ActionManager:
    def __init__(self):
        self.resources = {
            "FIREFIGHT": 2,
            "FIREBREAK": 2,
            "REPLANT": 1,
            "RESTORE_WATER": 2,
            "PROTECT": 2,
            "MONITOR": 1,
        }

    def can_afford(self, action_name):
        return self.resources.get(action_name, 0) > 0

    def spend(self, action_name):
        if self.resources.get(action_name, 0) <= 0:
            return False
        self.resources[action_name] -= 1
        return True

    def reset(self):
        self.resources = {
            "FIREFIGHT": 2,
            "FIREBREAK": 2,
            "REPLANT": 1,
            "RESTORE_WATER": 2,
            "PROTECT": 2,
            "MONITOR": 1,
        }
