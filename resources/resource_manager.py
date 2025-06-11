"""
Resource management system with flow-based inventory and production chains
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from core.config import GameConfig, Constants
from world.world_state import WorldState
from resources.stockpile import Stockpile, StockpileManager
from resources.production_chain import ProductionChain, ProductionManager
from resources.item import Item, ItemType

@dataclass
class ResourceFlow:
    """Represents a flow of resources between locations"""
    source: Tuple[int, int, int]
    destination: Tuple[int, int, int]
    item_type: str
    quantity: int
    flow_rate: float  # Items per second
    priority: int = 1
    
class ResourceManager:
    def __init__(self, config: GameConfig, world_state: WorldState):
        self.config = config
        self.world_state = world_state
        
        # Resource tracking
        self.global_inventory: Dict[str, int] = defaultdict(int)
        self.resource_flows: List[ResourceFlow] = []
        
        # Stockpile management
        self.stockpile_manager = StockpileManager(world_state)
        
        # Production management
        self.production_manager = ProductionManager(world_state)
        
        # Food decay system
        self.food_items: Dict[int, Item] = {}  # item_id -> Item
        self.next_item_id = 1
        
        # Temperature-aware storage
        self.temperature_zones: Dict[Tuple[int, int, int], float] = {}
        
        # Debug data
        self.flow_debug_data = {}
        
        self._initialize_production_chains()
        
    def _initialize_production_chains(self):
        """Initialize standard production chains"""
        # Ore -> Metal chain
        self.production_manager.add_chain(ProductionChain(
            name="iron_smelting",
            inputs={"iron_ore": 1, "coal": 1},
            outputs={"iron_bar": 1},
            time_required=10.0,
            skill_required=Constants.SKILL_CRAFTING,
            min_skill_level=1
        ))
        
        # Metal -> Tools chain
        self.production_manager.add_chain(ProductionChain(
            name="tool_forging",
            inputs={"iron_bar": 2},
            outputs={"pickaxe": 1},
            time_required=15.0,
            skill_required=Constants.SKILL_CRAFTING,
            min_skill_level=2
        ))
        
        # Food preparation
        self.production_manager.add_chain(ProductionChain(
            name="food_preparation",
            inputs={"raw_meat": 1},
            outputs={"prepared_meal": 1},
            time_required=5.0,
            skill_required=Constants.SKILL_FARMING,
            min_skill_level=1
        ))
        
    def update(self, dt: float):
        """Update resource management systems"""
        # Update stockpiles
        self.stockpile_manager.update(dt)
        
        # Update production
        self.production_manager.update(dt)
        
        # Update resource flows
        self._update_resource_flows(dt)
        
        # Update food decay
        self._update_food_decay(dt)
        
        # Update temperature zones
        self._update_temperature_zones(dt)
        
    def _update_resource_flows(self, dt: float):
        """Update resource flows between stockpiles"""
        flows_to_remove = []
        
        for i, flow in enumerate(self.resource_flows):
            # Calculate flow amount for this frame
            flow_amount = flow.flow_rate * dt
            actual_amount = min(flow_amount, flow.quantity)
            
            if actual_amount > 0:
                # Move resources
                source_stockpile = self.stockpile_manager.get_stockpile_at(flow.source)
                dest_stockpile = self.stockpile_manager.get_stockpile_at(flow.destination)
                
                if source_stockpile and dest_stockpile:
                    removed = source_stockpile.remove_item(flow.item_type, int(actual_amount))
                    if removed > 0:
                        dest_stockpile.add_item(flow.item_type, removed)
                        flow.quantity -= removed
                        
                        # Store debug data
                        if self.config.show_resource_flows:
                            flow_key = f"{flow.source}->{flow.destination}"
                            self.flow_debug_data[flow_key] = {
                                'item_type': flow.item_type,
                                'amount_moved': removed,
                                'remaining': flow.quantity
                            }
                            
            # Remove completed flows
            if flow.quantity <= 0:
                flows_to_remove.append(i)
                
        # Remove completed flows (in reverse order to maintain indices)
        for i in reversed(flows_to_remove):
            del self.resource_flows[i]
            
    def _update_food_decay(self, dt: float):
        """Update food decay based on temperature"""
        items_to_remove = []
        
        for item_id, item in self.food_items.items():
            if item.item_type.category == "food":
                # Get temperature at item location
                temp = self.world_state.get_temperature(*item.position)
                
                # Calculate decay rate based on temperature
                decay_rate = self.config.food_decay_rate
                if temp > Constants.TEMP_HOT:
                    decay_rate *= 3.0  # Decay faster in heat
                elif temp < Constants.TEMP_FREEZING:
                    decay_rate *= 0.1  # Decay slower when frozen
                    
                # Apply decay
                item.condition -= decay_rate * dt
                
                if item.condition <= 0:
                    items_to_remove.append(item_id)
                    
        # Remove spoiled items
        for item_id in items_to_remove:
            del self.food_items[item_id]
            
    def _update_temperature_zones(self, dt: float):
        """Update temperature zones for storage optimization"""
        # Sample temperature at key locations
        for stockpile in self.stockpile_manager.get_all_stockpiles():
            x, y, z = stockpile.position
            temp = self.world_state.get_temperature(x, y, z)
            self.temperature_zones[(x, y, z)] = temp
            
    def add_resource_flow(self, source: Tuple[int, int, int], destination: Tuple[int, int, int], 
                         item_type: str, quantity: int, priority: int = 1):
        """Add a new resource flow"""
        flow = ResourceFlow(
            source=source,
            destination=destination,
            item_type=item_type,
            quantity=quantity,
            flow_rate=10.0,  # Default flow rate
            priority=priority
        )
        
        # Insert based on priority (higher priority first)
        inserted = False
        for i, existing_flow in enumerate(self.resource_flows):
            if priority > existing_flow.priority:
                self.resource_flows.insert(i, flow)
                inserted = True
                break
                
        if not inserted:
            self.resource_flows.append(flow)
            
    def create_item(self, item_type_name: str, position: Tuple[int, int, int], 
                   quantity: int = 1) -> Item:
        """Create a new item"""
        item_type = ItemType.get_type(item_type_name)
        item = Item(
            item_id=self.next_item_id,
            item_type=item_type,
            position=position,
            quantity=quantity
        )
        
        self.next_item_id += 1
        
        # Track food items separately for decay
        if item_type.category == "food":
            self.food_items[item.item_id] = item
            
        return item
        
    def get_global_resource_count(self, resource_type: str) -> int:
        """Get total count of a resource type across all stockpiles"""
        total = 0
        for stockpile in self.stockpile_manager.get_all_stockpiles():
            total += stockpile.get_item_count(resource_type)
        return total
        
    def find_nearest_resource(self, position: Tuple[int, int, int], 
                            resource_type: str) -> Optional[Tuple[int, int, int]]:
        """Find the nearest stockpile containing the specified resource"""
        best_distance = float('inf')
        best_position = None
        
        for stockpile in self.stockpile_manager.get_all_stockpiles():
            if stockpile.get_item_count(resource_type) > 0:
                distance = self._calculate_distance(position, stockpile.position)
                if distance < best_distance:
                    best_distance = distance
                    best_position = stockpile.position
                    
        return best_position
        
    def _calculate_distance(self, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> float:
        """Calculate 3D distance between positions"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return (dx*dx + dy*dy + dz*dz) ** 0.5
        
    def request_production(self, chain_name: str, quantity: int = 1) -> bool:
        """Request production of items using a production chain"""
        return self.production_manager.queue_production(chain_name, quantity)
        
    def get_production_status(self) -> Dict[str, Any]:
        """Get current production status"""
        return self.production_manager.get_status()
        
    def create_stockpile(self, position: Tuple[int, int, int], size: Tuple[int, int, int],
                        allowed_items: List[str] = None) -> Stockpile:
        """Create a new stockpile"""
        return self.stockpile_manager.create_stockpile(position, size, allowed_items)
        
    def get_flow_debug_data(self) -> Dict[str, Any]:
        """Get resource flow debug data"""
        return self.flow_debug_data.copy()
        
    def serialize(self) -> Dict[str, Any]:
        """Serialize resource manager state"""
        return {
            'global_inventory': dict(self.global_inventory),
            'resource_flows': [
                {
                    'source': flow.source,
                    'destination': flow.destination,
                    'item_type': flow.item_type,
                    'quantity': flow.quantity,
                    'flow_rate': flow.flow_rate,
                    'priority': flow.priority
                }
                for flow in self.resource_flows
            ],
            'food_items': {str(k): v.serialize() for k, v in self.food_items.items()},
            'next_item_id': self.next_item_id,
            'stockpiles': self.stockpile_manager.serialize(),
            'production': self.production_manager.serialize()
        }
        
    def deserialize(self, data: Dict[str, Any]):
        """Deserialize resource manager state"""
        self.global_inventory = defaultdict(int, data['global_inventory'])
        self.next_item_id = data['next_item_id']
        
        # Restore resource flows
        self.resource_flows.clear()
        for flow_data in data['resource_flows']:
            flow = ResourceFlow(**flow_data)
            self.resource_flows.append(flow)
            
        # Restore food items
        self.food_items.clear()
        for item_id_str, item_data in data['food_items'].items():
            item_id = int(item_id_str)
            item = Item.deserialize(item_data)
            self.food_items[item_id] = item
            
        # Restore stockpiles and production
        self.stockpile_manager.deserialize(data['stockpiles'])
        self.production_manager.deserialize(data['production'])
