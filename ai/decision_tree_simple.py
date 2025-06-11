"""
AI decision tree for dwarf behavior - simplified version
"""

from dataclasses import dataclass
from core.config import GameConfig, Constants

@dataclass
class Decision:
    """Represents an AI decision"""
    action_type: str
    priority: float
    target_position: tuple = None
    work_type: str = None

class DecisionTree:
    """Makes decisions for dwarf AI"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        
    def make_decision(self, dwarf, world_state) -> Decision:
        """Make a decision for a dwarf based on current state"""
        # Simple decision making based on needs
        most_urgent_need = min(dwarf.needs, key=dwarf.needs.get)
        
        if dwarf.needs[most_urgent_need] < 30:
            if most_urgent_need == Constants.NEED_FOOD:
                return Decision("find_food", 1.0)
            elif most_urgent_need == Constants.NEED_DRINK:
                return Decision("find_drink", 1.0)
            elif most_urgent_need == Constants.NEED_SLEEP:
                return Decision("sleep", 0.8)
                
        # Default to wandering
        return Decision("wander", 0.1)
