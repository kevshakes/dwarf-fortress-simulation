"""
Simplified world state without numpy dependency
"""

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

@dataclass
class HistoricalEvent:
    """Represents a historical event"""
    year: int
    event_type: str
    description: str
    location: Optional[Tuple[int, int]] = None
    participants: List[str] = field(default_factory=list)

class WorldState:
    """Main world state container - simplified version"""
    
    def __init__(self, size: int, z_levels: int):
        self.size = size
        self.z_levels = z_levels
        
        # 3D tile array using nested lists instead of numpy
        self.tiles = []
        for x in range(size):
            x_layer = []
            for y in range(size):
                y_layer = []
                for z in range(z_levels):
                    y_layer.append(Tile())
                x_layer.append(y_layer)
            self.tiles.append(x_layer)
        
        # Environmental maps using nested lists
        self.biomes = [[None for _ in range(size)] for _ in range(size)]
        self.drainage_map = [[0.0 for _ in range(size)] for _ in range(size)]
        self.salinity_map = [[0.0 for _ in range(size)] for _ in range(size)]
        
        # Temperature map
        self.temperature_map = [[[20.0 for _ in range(z_levels)] for _ in range(size)] for _ in range(size)]
        
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
        return self.tiles[x][y][z]
        
    def set_tile(self, x: int, y: int, z: int, tile: Tile):
        """Set tile at coordinates"""
        if self.is_valid_coordinate(x, y, z):
            self.tiles[x][y][z] = tile
            
    def is_valid_coordinate(self, x: int, y: int, z: int) -> bool:
        """Check if coordinates are valid"""
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                0 <= z < self.z_levels)
                
    def get_biome(self, x: int, y: int) -> Optional[Biome]:
        """Get biome at surface coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.biomes[x][y]
        return None
        
    def set_biome(self, x: int, y: int, biome: Biome):
        """Set biome at surface coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.biomes[x][y] = biome
            
    def get_temperature(self, x: int, y: int, z: int) -> float:
        """Get temperature at coordinates"""
        if self.is_valid_coordinate(x, y, z):
            return self.temperature_map[x][y][z]
        return 20.0  # Default temperature
        
    def set_temperature(self, x: int, y: int, z: int, temperature: float):
        """Set temperature at coordinates"""
        if self.is_valid_coordinate(x, y, z):
            self.temperature_map[x][y][z] = temperature
            self.tiles[x][y][z].temperature = temperature
            
    def find_surface_level(self, x: int, y: int) -> int:
        """Find the surface level (highest non-empty tile) at given x,y"""
        for z in range(self.z_levels - 1, -1, -1):
            if self.get_tile(x, y, z).material != Constants.TILE_EMPTY:
                return z
        return 0
