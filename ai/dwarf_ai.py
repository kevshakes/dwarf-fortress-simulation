"""
Individual dwarf AI behavior
"""

from typing import Optional, List, Tuple, Any
from core.config import GameConfig
from world.world_state import WorldState
from ai.pathfinding import AStarPathfinder

class DwarfAI:
    """AI controller for individual dwarf"""
    
    def __init__(self, dwarf, world_state: WorldState, pathfinder: AStarPathfinder, config: GameConfig):
        self.dwarf = dwarf
        self.world_state = world_state
        self.pathfinder = pathfinder
        self.config = config
        
        self.current_task = None
        self.current_path = []
        self.path_index = 0
        
    def update(self, dt: float):
        """Update AI behavior"""
        if self.current_path and self.path_index < len(self.current_path):
            self._follow_path(dt)
            
    def execute_decision(self, decision):
        """Execute an AI decision"""
        if hasattr(decision, 'action_type'):
            if decision.action_type == "move_to":
                self._move_to(decision.target_position)
            elif decision.action_type == "work":
                self._start_work_task(decision.work_type)
                
    def _move_to(self, target_position: Tuple[int, int, int]):
        """Move to target position"""
        path = self.pathfinder.find_path(self.dwarf.position, target_position)
        if path:
            self.current_path = path
            self.path_index = 0
            
    def _follow_path(self, dt: float):
        """Follow current path"""
        if self.path_index < len(self.current_path):
            target = self.current_path[self.path_index]
            # Simple movement - just teleport for now
            self.dwarf.position = target
            self.path_index += 1
            
    def _start_work_task(self, work_type: str):
        """Start a work task"""
        self.current_task = work_type
        self.dwarf.is_working = True
