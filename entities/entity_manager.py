"""
Entity management system using Entity-Component architecture
"""

import random
from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass, field
from core.config import GameConfig, Constants
from world.world_state import WorldState
from entities.components import *
from entities.dwarf import Dwarf

class EntityManager:
    def __init__(self, config: GameConfig, world_state: WorldState):
        self.config = config
        self.world_state = world_state
        
        # Entity storage
        self.entities: Dict[int, Any] = {}
        self.next_entity_id = 1
        
        # Component storage (for ECS pattern)
        self.components: Dict[Type, Dict[int, Any]] = {}
        
        # Entity type indices for fast lookup
        self.entities_by_type: Dict[str, List[int]] = {}
        
    def create_entity(self, entity_type: str) -> int:
        """Create a new entity and return its ID"""
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        
        if entity_type not in self.entities_by_type:
            self.entities_by_type[entity_type] = []
        self.entities_by_type[entity_type].append(entity_id)
        
        return entity_id
        
    def destroy_entity(self, entity_id: int):
        """Destroy an entity and all its components"""
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            
            # Remove from type index
            entity_type = getattr(entity, 'entity_type', 'unknown')
            if entity_type in self.entities_by_type:
                if entity_id in self.entities_by_type[entity_type]:
                    self.entities_by_type[entity_type].remove(entity_id)
                    
            # Remove all components
            for component_type in self.components:
                if entity_id in self.components[component_type]:
                    del self.components[component_type][entity_id]
                    
            # Remove entity
            del self.entities[entity_id]
            
    def add_component(self, entity_id: int, component: Any):
        """Add a component to an entity"""
        component_type = type(component)
        
        if component_type not in self.components:
            self.components[component_type] = {}
            
        self.components[component_type][entity_id] = component
        
    def get_component(self, entity_id: int, component_type: Type) -> Optional[Any]:
        """Get a component from an entity"""
        if component_type in self.components:
            return self.components[component_type].get(entity_id)
        return None
        
    def has_component(self, entity_id: int, component_type: Type) -> bool:
        """Check if entity has a component"""
        return (component_type in self.components and 
                entity_id in self.components[component_type])
                
    def get_entities_with_component(self, component_type: Type) -> List[int]:
        """Get all entities that have a specific component"""
        if component_type in self.components:
            return list(self.components[component_type].keys())
        return []
        
    def create_dwarf(self, x: int, y: int, z: int) -> Dwarf:
        """Create a new dwarf entity"""
        # Find a suitable spawn location
        spawn_pos = self._find_spawn_location(x, y, z)
        if not spawn_pos:
            spawn_pos = (x, y, z)
            
        dwarf = Dwarf(
            entity_id=self.create_entity('dwarf'),
            position=spawn_pos,
            world_state=self.world_state
        )
        
        # Add to entities
        self.entities[dwarf.entity_id] = dwarf
        
        # Add components
        self.add_component(dwarf.entity_id, PositionComponent(*spawn_pos))
        self.add_component(dwarf.entity_id, MovementComponent())
        self.add_component(dwarf.entity_id, InventoryComponent())
        self.add_component(dwarf.entity_id, SkillsComponent())
        self.add_component(dwarf.entity_id, NeedsComponent())
        self.add_component(dwarf.entity_id, MoodComponent())
        
        return dwarf
        
    def create_initial_dwarves(self, count: int):
        """Create initial dwarf population"""
        # Find a good starting location (near surface, in a suitable biome)
        start_x = self.world_state.size // 2
        start_y = self.world_state.size // 2
        start_z = self.world_state.find_surface_level(start_x, start_y) + 1
        
        for i in range(count):
            # Spread dwarves around the starting area
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            
            dwarf_x = max(0, min(self.world_state.size - 1, start_x + offset_x))
            dwarf_y = max(0, min(self.world_state.size - 1, start_y + offset_y))
            
            dwarf = self.create_dwarf(dwarf_x, dwarf_y, start_z)
            print(f"Created dwarf {dwarf.name} at ({dwarf_x}, {dwarf_y}, {start_z})")
            
    def _find_spawn_location(self, x: int, y: int, z: int) -> Optional[tuple]:
        """Find a suitable spawn location near the given coordinates"""
        # Check if the given location is suitable
        if self._is_suitable_spawn(x, y, z):
            return (x, y, z)
            
        # Search in expanding radius
        for radius in range(1, 10):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:  # Only check perimeter
                        test_x, test_y = x + dx, y + dy
                        if self._is_suitable_spawn(test_x, test_y, z):
                            return (test_x, test_y, z)
                            
        return None
        
    def _is_suitable_spawn(self, x: int, y: int, z: int) -> bool:
        """Check if a location is suitable for spawning"""
        if not self.world_state.is_valid_coordinate(x, y, z):
            return False
            
        tile = self.world_state.get_tile(x, y, z)
        return tile.is_passable() and tile.water_level < 3
        
    def update(self, dt: float):
        """Update all entities"""
        for entity in self.entities.values():
            if hasattr(entity, 'update'):
                entity.update(dt)
                
    def get_entity(self, entity_id: int) -> Optional[Any]:
        """Get entity by ID"""
        return self.entities.get(entity_id)
        
    def get_entities_by_type(self, entity_type: str) -> List[Any]:
        """Get all entities of a specific type"""
        if entity_type in self.entities_by_type:
            return [self.entities[eid] for eid in self.entities_by_type[entity_type] 
                   if eid in self.entities]
        return []
        
    def get_all_entities(self) -> List[Any]:
        """Get all entities"""
        return list(self.entities.values())
        
    def get_visible_entities(self) -> List[Any]:
        """Get entities that should be rendered"""
        # For now, return all entities
        # In a full implementation, this would do frustum culling
        return self.get_all_entities()
        
    def get_entity_count(self) -> int:
        """Get total entity count"""
        return len(self.entities)
        
    def serialize(self) -> Dict[str, Any]:
        """Serialize entity manager state for saving"""
        return {
            'entities': {eid: entity.serialize() for eid, entity in self.entities.items()},
            'next_entity_id': self.next_entity_id,
            'entities_by_type': self.entities_by_type.copy()
        }
        
    def deserialize(self, data: Dict[str, Any]):
        """Deserialize entity manager state from save data"""
        self.entities.clear()
        self.components.clear()
        self.entities_by_type.clear()
        
        self.next_entity_id = data['next_entity_id']
        self.entities_by_type = data['entities_by_type'].copy()
        
        # Recreate entities
        for eid_str, entity_data in data['entities'].items():
            eid = int(eid_str)
            
            # Recreate dwarf entities
            if entity_data['type'] == 'dwarf':
                dwarf = Dwarf.deserialize(entity_data, self.world_state)
                self.entities[eid] = dwarf
                
                # Recreate components
                pos = entity_data['position']
                self.add_component(eid, PositionComponent(*pos))
                self.add_component(eid, MovementComponent())
                self.add_component(eid, InventoryComponent())
                self.add_component(eid, SkillsComponent())
                self.add_component(eid, NeedsComponent())
                self.add_component(eid, MoodComponent())
