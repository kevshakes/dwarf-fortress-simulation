"""
Spatial partitioning system for performance optimization
"""

from typing import List, Dict, Set, Tuple, Any
from collections import defaultdict
import math

class SpatialPartition:
    """Grid-based spatial partitioning for efficient entity queries"""
    
    def __init__(self, world_size: int, grid_size: int):
        self.world_size = world_size
        self.grid_size = grid_size
        self.cell_size = world_size / grid_size
        
        # Grid storage: grid[x][y][z] = set of entity_ids
        self.grid: Dict[Tuple[int, int, int], Set[int]] = defaultdict(set)
        
        # Entity position tracking
        self.entity_positions: Dict[int, Tuple[int, int, int]] = {}
        
    def update(self, entities: List[Any]):
        """Update spatial partitioning with current entity positions"""
        # Clear old positions
        self.grid.clear()
        self.entity_positions.clear()
        
        # Add entities to grid
        for entity in entities:
            if hasattr(entity, 'position') and hasattr(entity, 'entity_id'):
                self.add_entity(entity.entity_id, entity.position)
                
    def add_entity(self, entity_id: int, position: Tuple[int, int, int]):
        """Add entity to spatial grid"""
        grid_pos = self._world_to_grid(position)
        self.grid[grid_pos].add(entity_id)
        self.entity_positions[entity_id] = position
        
    def remove_entity(self, entity_id: int):
        """Remove entity from spatial grid"""
        if entity_id in self.entity_positions:
            position = self.entity_positions[entity_id]
            grid_pos = self._world_to_grid(position)
            self.grid[grid_pos].discard(entity_id)
            del self.entity_positions[entity_id]
            
    def move_entity(self, entity_id: int, old_position: Tuple[int, int, int], 
                   new_position: Tuple[int, int, int]):
        """Move entity from old position to new position"""
        old_grid_pos = self._world_to_grid(old_position)
        new_grid_pos = self._world_to_grid(new_position)
        
        if old_grid_pos != new_grid_pos:
            self.grid[old_grid_pos].discard(entity_id)
            self.grid[new_grid_pos].add(entity_id)
            
        self.entity_positions[entity_id] = new_position
        
    def query_radius(self, center: Tuple[int, int, int], radius: float) -> List[int]:
        """Get all entities within radius of center point"""
        entities = set()
        
        # Calculate grid bounds
        min_grid = self._world_to_grid((
            max(0, center[0] - radius),
            max(0, center[1] - radius),
            max(0, center[2] - radius)
        ))
        max_grid = self._world_to_grid((
            min(self.world_size - 1, center[0] + radius),
            min(self.world_size - 1, center[1] + radius),
            min(self.world_size - 1, center[2] + radius)
        ))
        
        # Check all grid cells in range
        for gx in range(min_grid[0], max_grid[0] + 1):
            for gy in range(min_grid[1], max_grid[1] + 1):
                for gz in range(min_grid[2], max_grid[2] + 1):
                    grid_pos = (gx, gy, gz)
                    if grid_pos in self.grid:
                        for entity_id in self.grid[grid_pos]:
                            if entity_id in self.entity_positions:
                                entity_pos = self.entity_positions[entity_id]
                                distance = self._calculate_distance(center, entity_pos)
                                if distance <= radius:
                                    entities.add(entity_id)
                                    
        return list(entities)
        
    def query_box(self, min_pos: Tuple[int, int, int], max_pos: Tuple[int, int, int]) -> List[int]:
        """Get all entities within a box region"""
        entities = set()
        
        min_grid = self._world_to_grid(min_pos)
        max_grid = self._world_to_grid(max_pos)
        
        for gx in range(min_grid[0], max_grid[0] + 1):
            for gy in range(min_grid[1], max_grid[1] + 1):
                for gz in range(min_grid[2], max_grid[2] + 1):
                    grid_pos = (gx, gy, gz)
                    if grid_pos in self.grid:
                        entities.update(self.grid[grid_pos])
                        
        return list(entities)
        
    def get_neighbors(self, entity_id: int, radius: float) -> List[int]:
        """Get neighboring entities within radius"""
        if entity_id not in self.entity_positions:
            return []
            
        position = self.entity_positions[entity_id]
        neighbors = self.query_radius(position, radius)
        
        # Remove self from neighbors
        if entity_id in neighbors:
            neighbors.remove(entity_id)
            
        return neighbors
        
    def _world_to_grid(self, world_pos: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert world coordinates to grid coordinates"""
        gx = int(world_pos[0] / self.cell_size)
        gy = int(world_pos[1] / self.cell_size)
        gz = int(world_pos[2] / self.cell_size)
        
        # Clamp to grid bounds
        gx = max(0, min(self.grid_size - 1, gx))
        gy = max(0, min(self.grid_size - 1, gy))
        gz = max(0, min(self.grid_size - 1, gz))
        
        return (gx, gy, gz)
        
    def _calculate_distance(self, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> float:
        """Calculate 3D distance between positions"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
        
    def resize_grid(self, new_grid_size: int):
        """Resize the spatial grid"""
        self.grid_size = new_grid_size
        self.cell_size = self.world_size / new_grid_size
        
        # Rebuild grid with new size
        old_positions = self.entity_positions.copy()
        self.grid.clear()
        self.entity_positions.clear()
        
        for entity_id, position in old_positions.items():
            self.add_entity(entity_id, position)
            
    def get_statistics(self) -> Dict[str, Any]:
        """Get spatial partitioning statistics"""
        total_cells = len(self.grid)
        total_entities = len(self.entity_positions)
        
        if total_cells > 0:
            entities_per_cell = [len(entities) for entities in self.grid.values()]
            avg_entities_per_cell = sum(entities_per_cell) / len(entities_per_cell)
            max_entities_per_cell = max(entities_per_cell)
        else:
            avg_entities_per_cell = 0
            max_entities_per_cell = 0
            
        return {
            'grid_size': self.grid_size,
            'cell_size': self.cell_size,
            'total_cells_used': total_cells,
            'total_entities': total_entities,
            'avg_entities_per_cell': avg_entities_per_cell,
            'max_entities_per_cell': max_entities_per_cell
        }
