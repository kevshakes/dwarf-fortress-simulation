"""
Stockpile management system
"""

from typing import Dict, List, Tuple, Any
from collections import defaultdict

class Stockpile:
    """Individual stockpile for storing items"""
    
    def __init__(self, position: Tuple[int, int, int], size: Tuple[int, int, int], 
                 allowed_items: List[str] = None):
        self.position = position
        self.size = size
        self.allowed_items = allowed_items or []
        self.items: Dict[str, int] = defaultdict(int)
        self.max_capacity = size[0] * size[1] * size[2] * 10  # 10 items per tile
        
    def add_item(self, item_type: str, quantity: int) -> int:
        """Add items to stockpile, return actual amount added"""
        if self.allowed_items and item_type not in self.allowed_items:
            return 0
            
        current_total = sum(self.items.values())
        available_space = self.max_capacity - current_total
        actual_added = min(quantity, available_space)
        
        self.items[item_type] += actual_added
        return actual_added
        
    def remove_item(self, item_type: str, quantity: int) -> int:
        """Remove items from stockpile, return actual amount removed"""
        available = self.items.get(item_type, 0)
        actual_removed = min(quantity, available)
        
        self.items[item_type] -= actual_removed
        if self.items[item_type] <= 0:
            del self.items[item_type]
            
        return actual_removed
        
    def get_item_count(self, item_type: str) -> int:
        """Get count of specific item type"""
        return self.items.get(item_type, 0)

class StockpileManager:
    """Manages all stockpiles"""
    
    def __init__(self, world_state):
        self.world_state = world_state
        self.stockpiles: List[Stockpile] = []
        
    def create_stockpile(self, position: Tuple[int, int, int], size: Tuple[int, int, int],
                        allowed_items: List[str] = None) -> Stockpile:
        """Create a new stockpile"""
        stockpile = Stockpile(position, size, allowed_items)
        self.stockpiles.append(stockpile)
        return stockpile
        
    def get_stockpile_at(self, position: Tuple[int, int, int]) -> Stockpile:
        """Get stockpile at position"""
        for stockpile in self.stockpiles:
            if stockpile.position == position:
                return stockpile
        return None
        
    def get_all_stockpiles(self) -> List[Stockpile]:
        """Get all stockpiles"""
        return self.stockpiles
        
    def update(self, dt: float):
        """Update stockpiles"""
        pass
        
    def serialize(self) -> Dict[str, Any]:
        """Serialize stockpiles"""
        return {'stockpiles': []}
        
    def deserialize(self, data: Dict[str, Any]):
        """Deserialize stockpiles"""
        pass
