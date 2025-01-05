from typing import List, Dict

class ActionCombination:
    def __init__(self, name: str, action: str, ingredients: List[str], pre_condition: Dict):
        self.name = name
        self.action = action
        self.ingredients = ingredients
        self.pre_conditions = pre_condition
