"""
Item system
"""

from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class ItemType:
    """Defines an item type"""
    name: str
    category: str
    weight: float
    value: int
    
    @classmethod
    def get_type(cls, name: str) -> 'ItemType':
        """Get item type by name"""
        # Simple item types for now
        item_types = {
            'iron_ore': ItemType('iron_ore', 'material', 2.0, 1),
            'iron_bar': ItemType('iron_bar', 'material', 5.0, 10),
            'pickaxe': ItemType('pickaxe', 'tool', 3.0, 50),
            'raw_meat': ItemType('raw_meat', 'food', 1.0, 5),
            'prepared_meal': ItemType('prepared_meal', 'food', 0.5, 15)
        }
        return item_types.get(name, ItemType(name, 'unknown', 1.0, 1))

class Item:
    """Individual item instance"""
    
    def __init__(self, item_id: int, item_type: ItemType, position: Tuple[int, int, int], 
                 quantity: int = 1):
        self.item_id = item_id
        self.item_type = item_type
        self.position = position
        self.quantity = quantity
        self.condition = 1.0  # 0-1 scale
        
    def serialize(self) -> Dict[str, Any]:
        """Serialize item"""
        return {
            'item_id': self.item_id,
            'type_name': self.item_type.name,
            'position': self.position,
            'quantity': self.quantity,
            'condition': self.condition
        }
        
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Item':
        """Deserialize item"""
        item_type = ItemType.get_type(data['type_name'])
        item = cls(
            data['item_id'],
            item_type,
            tuple(data['position']),
            data['quantity']
        )
        item.condition = data['condition']
        return item
