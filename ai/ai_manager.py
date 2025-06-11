"""
AI Manager coordinating all AI systems
"""

import time
from typing import Dict, List, Any, Optional
from core.config import GameConfig
from world.world_state import WorldState
from entities.entity_manager import EntityManager
from ai.pathfinding import AStarPathfinder
from ai.dwarf_ai import DwarfAI
from ai.needs_system import NeedsSystem
from ai.relationship_system import RelationshipSystem
from ai.decision_tree import DecisionTree

class AIManager:
    def __init__(self, config: GameConfig, world_state: WorldState, entity_manager: EntityManager):
        self.config = config
        self.world_state = world_state
        self.entity_manager = entity_manager
        
        # AI Systems
        self.pathfinder = AStarPathfinder(world_state, config.pathfinding_max_iterations)
        self.needs_system = NeedsSystem(config)
        self.relationship_system = RelationshipSystem(config)
        self.decision_tree = DecisionTree(config)
        
        # AI instances for each dwarf
        self.dwarf_ais: Dict[int, DwarfAI] = {}
        
        # Timing
        self.last_ai_update = 0
        self.last_relationship_update = 0
        
        # Debug data
        self.pathfinding_debug_data = {}
        self.decision_debug_data = {}
        
    def update(self, dt: float):
        """Update all AI systems"""
        current_time = time.time()
        
        # Update AI decisions at specified interval
        if current_time - self.last_ai_update >= self.config.ai_decision_interval:
            self.update_ai_decisions(dt)
            self.last_ai_update = current_time
            
        # Update relationships less frequently
        if current_time - self.last_relationship_update >= self.config.relationship_update_interval:
            self.relationship_system.update(dt)
            self.last_relationship_update = current_time
            
        # Update individual dwarf AIs
        for dwarf_ai in self.dwarf_ais.values():
            dwarf_ai.update(dt)
            
    def update_ai_decisions(self, dt: float):
        """Update AI decision making for all dwarves"""
        dwarves = self.entity_manager.get_entities_by_type('dwarf')
        
        for dwarf in dwarves:
            if dwarf.entity_id not in self.dwarf_ais:
                self.create_dwarf_ai(dwarf)
                
            dwarf_ai = self.dwarf_ais[dwarf.entity_id]
            
            # Update needs
            self.needs_system.update_needs(dwarf, dt)
            
            # Make decisions based on current state
            decision = self.decision_tree.make_decision(dwarf, self.world_state)
            dwarf_ai.execute_decision(decision)
            
            # Store debug data
            if self.config.show_ai_decisions:
                self.decision_debug_data[dwarf.entity_id] = {
                    'current_decision': decision.action_type,
                    'needs': dwarf.needs.copy(),
                    'mood': dwarf.mood,
                    'current_task': dwarf_ai.current_task
                }
                
    def create_dwarf_ai(self, dwarf):
        """Create AI instance for a dwarf"""
        dwarf_ai = DwarfAI(
            dwarf, 
            self.world_state, 
            self.pathfinder, 
            self.config
        )
        self.dwarf_ais[dwarf.entity_id] = dwarf_ai
        
    def find_path(self, start: tuple, goal: tuple, entity_id: int = None) -> Optional[List[tuple]]:
        """Find path between two points"""
        path = self.pathfinder.find_path(start, goal)
        
        # Store debug data
        if self.config.show_pathfinding and entity_id:
            self.pathfinding_debug_data[entity_id] = {
                'start': start,
                'goal': goal,
                'path': path,
                'path_length': len(path) if path else 0
            }
            
        return path
        
    def get_pathfinding_cache_size(self) -> int:
        """Get current pathfinding cache size"""
        return self.pathfinder.get_cache_size()
        
    def get_pathfinding_debug_data(self) -> Dict[str, Any]:
        """Get pathfinding debug data"""
        return self.pathfinding_debug_data.copy()
        
    def get_decision_debug_data(self) -> Dict[str, Any]:
        """Get AI decision debug data"""
        return self.decision_debug_data.copy()
        
    def reinitialize(self, world_state: WorldState, entity_manager: EntityManager):
        """Reinitialize AI systems after loading"""
        self.world_state = world_state
        self.entity_manager = entity_manager
        self.pathfinder.reinitialize(world_state)
        
        # Recreate dwarf AIs
        self.dwarf_ais.clear()
        dwarves = entity_manager.get_entities_by_type('dwarf')
        for dwarf in dwarves:
            self.create_dwarf_ai(dwarf)
