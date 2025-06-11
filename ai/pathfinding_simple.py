"""
A* pathfinding with 3D z-level navigation - simplified version
"""

import heapq
import math
from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass

@dataclass
class PathNode:
    """Node in the pathfinding graph"""
    position: Tuple[int, int, int]
    g_cost: float  # Cost from start
    h_cost: float  # Heuristic cost to goal
    f_cost: float  # Total cost
    parent: Optional['PathNode'] = None
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class AStarPathfinder:
    def __init__(self, world_state, max_iterations: int = 1000):
        self.world_state = world_state
        self.max_iterations = max_iterations
        
        # Pathfinding cache
        self.path_cache: Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], List[Tuple[int, int, int]]] = {}
        self.cache_max_size = 1000
        
    def find_path(self, start: Tuple[int, int, int], goal: Tuple[int, int, int]) -> Optional[List[Tuple[int, int, int]]]:
        """Find path from start to goal using A* algorithm"""
        # Check cache first
        cache_key = (start, goal)
        if cache_key in self.path_cache:
            return self.path_cache[cache_key].copy()
            
        # Validate start and goal
        if not self._is_valid_position(start) or not self._is_valid_position(goal):
            return None
            
        if not self._is_passable(start) or not self._is_passable(goal):
            return None
            
        # A* algorithm
        open_set = []
        closed_set: Set[Tuple[int, int, int]] = set()
        
        start_node = PathNode(
            position=start,
            g_cost=0,
            h_cost=self._heuristic(start, goal),
            f_cost=0
        )
        start_node.f_cost = start_node.g_cost + start_node.h_cost
        
        heapq.heappush(open_set, start_node)
        node_map: Dict[Tuple[int, int, int], PathNode] = {start: start_node}
        
        iterations = 0
        
        while open_set and iterations < self.max_iterations:
            iterations += 1
            current_node = heapq.heappop(open_set)
            
            if current_node.position in closed_set:
                continue
                
            closed_set.add(current_node.position)
            
            # Check if we reached the goal
            if current_node.position == goal:
                path = self._reconstruct_path(current_node)
                self._cache_path(cache_key, path)
                return path
                
            # Explore neighbors
            for neighbor_pos in self._get_neighbors(current_node.position):
                if neighbor_pos in closed_set or not self._is_passable(neighbor_pos):
                    continue
                    
                movement_cost = self._get_movement_cost(current_node.position, neighbor_pos)
                tentative_g_cost = current_node.g_cost + movement_cost
                
                if neighbor_pos in node_map:
                    neighbor_node = node_map[neighbor_pos]
                    if tentative_g_cost < neighbor_node.g_cost:
                        neighbor_node.g_cost = tentative_g_cost
                        neighbor_node.f_cost = neighbor_node.g_cost + neighbor_node.h_cost
                        neighbor_node.parent = current_node
                else:
                    neighbor_node = PathNode(
                        position=neighbor_pos,
                        g_cost=tentative_g_cost,
                        h_cost=self._heuristic(neighbor_pos, goal),
                        f_cost=0,
                        parent=current_node
                    )
                    neighbor_node.f_cost = neighbor_node.g_cost + neighbor_node.h_cost
                    node_map[neighbor_pos] = neighbor_node
                    heapq.heappush(open_set, neighbor_node)
                    
        # No path found
        return None
        
    def _get_neighbors(self, position: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Get valid neighboring positions including z-level movement"""
        x, y, z = position
        neighbors = []
        
        # Horizontal movement (same z-level)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_pos = (x + dx, y + dy, z)
            if self._is_valid_position(new_pos):
                neighbors.append(new_pos)
                
        # Vertical movement (z-level changes)
        # Can move up if there's a ramp or stairs
        if z < self.world_state.z_levels - 1:
            up_pos = (x, y, z + 1)
            if self._can_move_vertically(position, up_pos):
                neighbors.append(up_pos)
                
        # Can move down if there's a ramp, stairs, or it's safe to fall
        if z > 0:
            down_pos = (x, y, z - 1)
            if self._can_move_vertically(position, down_pos):
                neighbors.append(down_pos)
                
        return neighbors
        
    def _can_move_vertically(self, from_pos: Tuple[int, int, int], to_pos: Tuple[int, int, int]) -> bool:
        """Check if vertical movement is possible"""
        from_tile = self.world_state.get_tile(*from_pos)
        to_tile = self.world_state.get_tile(*to_pos)
        
        # Can't move to solid tiles
        if not to_tile.is_passable():
            return False
            
        # For now, allow vertical movement if both tiles are passable
        # In a full implementation, you'd check for ramps, stairs, etc.
        return True
        
    def _is_valid_position(self, position: Tuple[int, int, int]) -> bool:
        """Check if position is within world bounds"""
        x, y, z = position
        return self.world_state.is_valid_coordinate(x, y, z)
        
    def _is_passable(self, position: Tuple[int, int, int]) -> bool:
        """Check if position can be moved through"""
        tile = self.world_state.get_tile(*position)
        return tile.is_passable()
        
    def _get_movement_cost(self, from_pos: Tuple[int, int, int], to_pos: Tuple[int, int, int]) -> float:
        """Calculate movement cost between two adjacent positions"""
        from_tile = self.world_state.get_tile(*from_pos)
        to_tile = self.world_state.get_tile(*to_pos)
        
        # Base cost
        cost = to_tile.get_movement_cost()
        
        # Diagonal movement costs more
        dx = abs(to_pos[0] - from_pos[0])
        dy = abs(to_pos[1] - from_pos[1])
        dz = abs(to_pos[2] - from_pos[2])
        
        if dx + dy > 1:  # Diagonal movement
            cost *= 1.414  # sqrt(2)
            
        # Vertical movement costs more
        if dz > 0:
            cost *= 2.0
            
        return cost
        
    def _heuristic(self, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> float:
        """Calculate heuristic distance (3D Manhattan distance)"""
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        dz = abs(pos1[2] - pos2[2])
        
        # Use 3D Euclidean distance as heuristic
        return math.sqrt(dx*dx + dy*dy + dz*dz)
        
    def _reconstruct_path(self, goal_node: PathNode) -> List[Tuple[int, int, int]]:
        """Reconstruct path from goal node back to start"""
        path = []
        current = goal_node
        
        while current is not None:
            path.append(current.position)
            current = current.parent
            
        path.reverse()
        return path
        
    def _cache_path(self, cache_key: Tuple[Tuple[int, int, int], Tuple[int, int, int]], path: List[Tuple[int, int, int]]):
        """Cache the found path"""
        if len(self.path_cache) >= self.cache_max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self.path_cache))
            del self.path_cache[oldest_key]
            
        self.path_cache[cache_key] = path.copy()
        
    def get_cache_size(self) -> int:
        """Get current cache size"""
        return len(self.path_cache)
        
    def clear_cache(self):
        """Clear pathfinding cache"""
        self.path_cache.clear()
        
    def reinitialize(self, world_state):
        """Reinitialize pathfinder with new world state"""
        self.world_state = world_state
        self.clear_cache()
