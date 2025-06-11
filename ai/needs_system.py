"""
Dwarf needs management system
"""

from core.config import GameConfig, Constants

class NeedsSystem:
    """Manages dwarf needs and their effects"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        
    def update_needs(self, dwarf, dt: float):
        """Update dwarf needs over time"""
        # This is handled in the dwarf class itself
        pass
        
    def get_most_urgent_need(self, dwarf) -> str:
        """Get the most urgent need for a dwarf"""
        min_need = min(dwarf.needs.values())
        for need, value in dwarf.needs.items():
            if value == min_need:
                return need
        return Constants.NEED_FOOD
