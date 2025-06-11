"""
World state representation and management
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from core.config import Constants

@dataclass
class Tile:
    """Represents a single tile in the world"""
    material: int = Constants.TILE_EMPTY
    hardness: int = 0
    stability: float = 1.0
    temperature: float = 20.0
    water_level: int = 0  # 0-7 water levels
    minerals: Dict[str, int] = field(default_factory=dict)
    
    # Structural properties
    is_constructed: bool = False
    construction_material: str = ""
    
    # Designations
    is_designated_for_mining: bool = False
    is_designated_for_construction: bool = False
    
    def is_passable(self) -> bool:
        """Check if this tile can be passed through"""
        return self.material == Constants.TILE_EMPTY or self.water_level < 7
        
    def is_solid(self) -> bool:
        """Check if this tile is solid"""
        return self.material in [Constants.TILE_STONE, Constants.TILE_SOIL]
        
    def get_movement_cost(self) -> float:
        """Get movement cost for pathfinding"""
        if not self.is_passable():
            return float('inf')
        
        cost = 1.0
        if self.water_level > 0:
            cost += self.water_level * 0.5
        if self.material == Constants.TILE_SOIL:
            cost += 0.2
            
        return cost

@dataclass
class Biome:
    """Represents a biome with environmental properties"""
    type: str
    temperature: float
    humidity: float
    elevation: float
    
    def get_growth_rate(self) -> float:
        """Get plant growth rate modifier for this biome"""
        if self.type == Constants.BIOME_FOREST:
            return 1.2
        elif self.type == Constants.BIOME_SWAMP:
            return 1.5
        elif self.type == Constants.BIOME_DESERT:
            return 0.3
        elif self.type == Constants.BIOME_MOUNTAIN:
            return 0.8
        return 1.0

@dataclass
class HistoricalEvent:
    """Represents a historical event"""
    year: int
    event_type: str
    description: str
    location: Optional[Tuple[int, int]] = None
    participants: List[str] = field(default_factory=list)

class WorldState:
    """Main world state container"""
    
    def __init__(self, size: int, z_levels: int):
        self.size = size
        self.z_levels = z_levels
        
        # 3D tile array
        self.tiles = np.empty((size, size, z_levels), dtype=object)
        for x in range(size):
            for y in range(size):
                for z in range(z_levels):
                    self.tiles[x, y, z] = Tile()
        
        # Environmental maps
        self.biomes = np.empty((size, size), dtype=object)
        self.drainage_map = np.zeros((size, size), dtype=np.float32)
        self.salinity_map = np.zeros((size, size), dtype=np.float32)
        
        # Temperature is stored per tile, but we also maintain a quick lookup
        self.temperature_map = np.zeros((size, size, z_levels), dtype=np.float32)
        
        # Historical data
        self.history: List[HistoricalEvent] = []
        self.current_year = 0
        
        # Civilization data
        self.civilizations: Dict[str, Any] = {}
        self.trade_routes: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        
    def get_tile(self, x: int, y: int, z: int) -> Tile:
        """Get tile at coordinates"""
        if not self.is_valid_coordinate(x, y, z):
            # Return empty tile for out-of-bounds
            return Tile()
        return self.tiles[x, y, z]
        
    def set_tile(self, x: int, y: int, z: int, tile: Tile):
        """Set tile at coordinates"""
        if self.is_valid_coordinate(x, y, z):
            self.tiles[x, y, z] = tile
            
    def is_valid_coordinate(self, x: int, y: int, z: int) -> bool:
        """Check if coordinates are valid"""
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                0 <= z < self.z_levels)
                
    def get_biome(self, x: int, y: int) -> Optional[Biome]:
        """Get biome at surface coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.biomes[x, y]
        return None
        
    def set_biome(self, x: int, y: int, biome: Biome):
        """Set biome at surface coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.biomes[x, y] = biome
            
    def get_drainage(self, x: int, y: int) -> float:
        """Get drainage value at coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.drainage_map[x, y]
        return 0.0
        
    def set_drainage(self, x: int, y: int, value: float):
        """Set drainage value at coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.drainage_map[x, y] = value
            
    def get_salinity(self, x: int, y: int) -> float:
        """Get salinity value at coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.salinity_map[x, y]
        return 0.0
        
    def set_salinity(self, x: int, y: int, value: float):
        """Set salinity value at coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.salinity_map[x, y] = value
            
    def get_temperature(self, x: int, y: int, z: int) -> float:
        """Get temperature at coordinates"""
        if self.is_valid_coordinate(x, y, z):
            return self.temperature_map[x, y, z]
        return 20.0  # Default temperature
        
    def set_temperature(self, x: int, y: int, z: int, temperature: float):
        """Set temperature at coordinates"""
        if self.is_valid_coordinate(x, y, z):
            self.temperature_map[x, y, z] = temperature
            self.tiles[x, y, z].temperature = temperature
            
    def get_neighbors(self, x: int, y: int, z: int, include_diagonals: bool = True) -> List[Tuple[int, int, int]]:
        """Get neighboring coordinates"""
        neighbors = []
        
        if include_diagonals:
            offsets = [(-1, -1, 0), (-1, 0, 0), (-1, 1, 0),
                      (0, -1, 0),           (0, 1, 0),
                      (1, -1, 0), (1, 0, 0), (1, 1, 0),
                      (0, 0, -1), (0, 0, 1)]  # Include vertical neighbors
        else:
            offsets = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
            
        for dx, dy, dz in offsets:
            nx, ny, nz = x + dx, y + dy, z + dz
            if self.is_valid_coordinate(nx, ny, nz):
                neighbors.append((nx, ny, nz))
                
        return neighbors
        
    def find_surface_level(self, x: int, y: int) -> int:
        """Find the surface level (highest non-empty tile) at given x,y"""
        for z in range(self.z_levels - 1, -1, -1):
            if self.get_tile(x, y, z).material != Constants.TILE_EMPTY:
                return z
        return 0
        
    def is_tile_supported(self, x: int, y: int, z: int) -> bool:
        """Check if a tile has adequate structural support"""
        tile = self.get_tile(x, y, z)
        if not tile.is_solid():
            return True  # Empty tiles don't need support
            
        # Check for support from below
        if z > 0:
            below = self.get_tile(x, y, z - 1)
            if below.is_solid():
                return True
                
        # Check for adjacent support
        adjacent_support = 0
        for nx, ny, nz in self.get_neighbors(x, y, z, include_diagonals=False):
            if nz == z:  # Same level
                neighbor = self.get_tile(nx, ny, nz)
                if neighbor.is_solid():
                    adjacent_support += 1
                    
        return adjacent_support >= 2  # Need at least 2 adjacent supports
        
    def add_historical_event(self, event: HistoricalEvent):
        """Add a historical event"""
        self.history.append(event)
        self.history.sort(key=lambda e: e.year)
        
    def get_events_in_year(self, year: int) -> List[HistoricalEvent]:
        """Get all events that occurred in a specific year"""
        return [event for event in self.history if event.year == year]
        
    def get_events_at_location(self, x: int, y: int) -> List[HistoricalEvent]:
        """Get all events that occurred at a specific location"""
        return [event for event in self.history 
                if event.location and event.location == (x, y)]
