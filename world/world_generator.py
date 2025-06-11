"""
Procedural world generation using 3D Perlin noise
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from core.config import GameConfig, Constants
from world.world_state import WorldState, Tile, Biome
from utils.noise import PerlinNoise3D
from utils.history_generator import HistoryGenerator

@dataclass
class GenerationParams:
    """Parameters for world generation"""
    terrain_scale: float = 0.05
    biome_scale: float = 0.02
    mineral_scale: float = 0.08
    drainage_scale: float = 0.03
    salinity_scale: float = 0.04
    temperature_scale: float = 0.01

class WorldGenerator:
    def __init__(self, config: GameConfig):
        self.config = config
        self.params = GenerationParams()
        self.noise = PerlinNoise3D(config.noise_seed)
        self.history_generator = HistoryGenerator(config.noise_seed)
        
    def generate(self) -> WorldState:
        """Generate a complete world"""
        print("Generating terrain...")
        world_state = WorldState(self.config.world_size, self.config.z_levels)
        
        # Generate base terrain
        self._generate_terrain(world_state)
        
        # Generate biomes
        print("Generating biomes...")
        self._generate_biomes(world_state)
        
        # Generate mineral veins
        print("Generating mineral deposits...")
        self._generate_minerals(world_state)
        
        # Generate water features
        print("Generating water features...")
        self._generate_water(world_state)
        
        # Generate temperature map
        print("Generating temperature map...")
        self._generate_temperature(world_state)
        
        # Generate historical timeline
        print("Generating history...")
        world_state.history = self.history_generator.generate_history(world_state)
        
        print("World generation complete!")
        return world_state
        
    def _generate_terrain(self, world_state: WorldState):
        """Generate 3D terrain using Perlin noise"""
        size = world_state.size
        z_levels = world_state.z_levels
        
        for x in range(size):
            for y in range(size):
                # Generate height map
                height_noise = self.noise.sample(
                    x * self.params.terrain_scale,
                    y * self.params.terrain_scale,
                    0
                )
                
                # Convert to height (0-1 range to 0-z_levels)
                surface_height = int((height_noise + 1) * 0.5 * z_levels * 0.8)
                surface_height = max(1, min(z_levels - 1, surface_height))
                
                for z in range(z_levels):
                    tile = world_state.get_tile(x, y, z)
                    
                    if z < surface_height:
                        # Underground - determine stone vs soil
                        density_noise = self.noise.sample(
                            x * self.params.terrain_scale * 2,
                            y * self.params.terrain_scale * 2,
                            z * self.params.terrain_scale * 2
                        )
                        
                        if density_noise > 0.2:
                            tile.material = Constants.TILE_STONE
                            tile.hardness = 5 + int(density_noise * 5)
                        else:
                            tile.material = Constants.TILE_SOIL
                            tile.hardness = 1 + int(abs(density_noise) * 3)
                    else:
                        # Above ground - empty space
                        tile.material = Constants.TILE_EMPTY
                        tile.hardness = 0
                        
                    # Set stability based on surrounding tiles
                    tile.stability = self._calculate_stability(world_state, x, y, z)
                    
    def _generate_biomes(self, world_state: WorldState):
        """Generate biome classification"""
        size = world_state.size
        
        for x in range(size):
            for y in range(size):
                # Sample multiple noise layers for biome determination
                temperature = self.noise.sample(
                    x * self.params.biome_scale,
                    y * self.params.biome_scale,
                    100  # Different z offset for temperature
                )
                
                humidity = self.noise.sample(
                    x * self.params.biome_scale,
                    y * self.params.biome_scale,
                    200  # Different z offset for humidity
                )
                
                elevation = self._get_surface_elevation(world_state, x, y)
                elevation_factor = elevation / world_state.z_levels
                
                # Determine biome based on temperature, humidity, and elevation
                biome = self._classify_biome(temperature, humidity, elevation_factor)
                world_state.set_biome(x, y, biome)
                
    def _generate_minerals(self, world_state: WorldState):
        """Generate mineral veins and deposits"""
        size = world_state.size
        z_levels = world_state.z_levels
        
        # Define mineral types and their properties
        minerals = {
            'iron': {'rarity': 0.3, 'depth_preference': 0.4},
            'copper': {'rarity': 0.4, 'depth_preference': 0.3},
            'gold': {'rarity': 0.1, 'depth_preference': 0.6},
            'silver': {'rarity': 0.15, 'depth_preference': 0.5},
            'coal': {'rarity': 0.5, 'depth_preference': 0.2},
        }
        
        for mineral_name, properties in minerals.items():
            for x in range(size):
                for y in range(size):
                    for z in range(z_levels):
                        # Only place minerals in stone
                        tile = world_state.get_tile(x, y, z)
                        if tile.material != Constants.TILE_STONE:
                            continue
                            
                        # Calculate mineral probability
                        depth_factor = z / z_levels
                        depth_bonus = abs(depth_factor - properties['depth_preference'])
                        depth_bonus = 1.0 - depth_bonus
                        
                        mineral_noise = self.noise.sample(
                            x * self.params.mineral_scale,
                            y * self.params.mineral_scale,
                            z * self.params.mineral_scale + hash(mineral_name) % 1000
                        )
                        
                        probability = properties['rarity'] * depth_bonus
                        if mineral_noise > (1.0 - probability):
                            tile.minerals[mineral_name] = min(10, int((mineral_noise + 1) * 5))
                            
    def _generate_water(self, world_state: WorldState):
        """Generate water features and drainage"""
        size = world_state.size
        
        for x in range(size):
            for y in range(size):
                # Generate drainage map
                drainage = self.noise.sample(
                    x * self.params.drainage_scale,
                    y * self.params.drainage_scale,
                    300
                )
                
                # Generate salinity map
                salinity = self.noise.sample(
                    x * self.params.salinity_scale,
                    y * self.params.salinity_scale,
                    400
                )
                
                # Set drainage and salinity for the column
                world_state.set_drainage(x, y, (drainage + 1) * 0.5)
                world_state.set_salinity(x, y, max(0, salinity))
                
                # Place water based on drainage and elevation
                surface_z = self._get_surface_elevation(world_state, x, y)
                if drainage > 0.3 and surface_z < world_state.z_levels * 0.3:
                    # Place water on surface
                    water_tile = world_state.get_tile(x, y, surface_z)
                    water_tile.water_level = min(7, int((drainage + 1) * 4))
                    
    def _generate_temperature(self, world_state: WorldState):
        """Generate temperature map"""
        size = world_state.size
        z_levels = world_state.z_levels
        
        for x in range(size):
            for y in range(size):
                for z in range(z_levels):
                    # Base temperature from noise
                    temp_noise = self.noise.sample(
                        x * self.params.temperature_scale,
                        y * self.params.temperature_scale,
                        z * self.params.temperature_scale + 500
                    )
                    
                    # Depth affects temperature (deeper = warmer)
                    depth_factor = z / z_levels
                    base_temp = Constants.TEMP_NORMAL + (temp_noise * 10)
                    depth_temp = depth_factor * 20  # Gets warmer deeper
                    
                    final_temp = base_temp + depth_temp
                    
                    # Special case for magma near bottom
                    if z < 3 and temp_noise > 0.7:
                        final_temp = Constants.TEMP_MAGMA
                        tile = world_state.get_tile(x, y, z)
                        tile.material = Constants.TILE_MAGMA
                        
                    world_state.set_temperature(x, y, z, final_temp)
                    
    def _classify_biome(self, temperature: float, humidity: float, elevation: float) -> Biome:
        """Classify biome based on environmental factors"""
        # Normalize values to 0-1 range
        temp = (temperature + 1) * 0.5
        humid = (humidity + 1) * 0.5
        
        if elevation > 0.7:
            return Biome(Constants.BIOME_MOUNTAIN, temp, humid, elevation)
        elif temp < 0.3 and humid > 0.6:
            return Biome(Constants.BIOME_SWAMP, temp, humid, elevation)
        elif temp > 0.7 and humid < 0.3:
            return Biome(Constants.BIOME_DESERT, temp, humid, elevation)
        else:
            return Biome(Constants.BIOME_FOREST, temp, humid, elevation)
            
    def _get_surface_elevation(self, world_state: WorldState, x: int, y: int) -> int:
        """Get the surface elevation at given coordinates"""
        for z in range(world_state.z_levels - 1, -1, -1):
            tile = world_state.get_tile(x, y, z)
            if tile.material != Constants.TILE_EMPTY:
                return z
        return 0
        
    def _calculate_stability(self, world_state: WorldState, x: int, y: int, z: int) -> float:
        """Calculate structural stability of a tile"""
        if world_state.get_tile(x, y, z).material == Constants.TILE_EMPTY:
            return 1.0
            
        # Check surrounding tiles for support
        support_count = 0
        total_neighbors = 0
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                        
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if (0 <= nx < world_state.size and 
                        0 <= ny < world_state.size and 
                        0 <= nz < world_state.z_levels):
                        
                        neighbor = world_state.get_tile(nx, ny, nz)
                        total_neighbors += 1
                        if neighbor.material in [Constants.TILE_STONE, Constants.TILE_SOIL]:
                            support_count += 1
                            
        return support_count / max(1, total_neighbors) if total_neighbors > 0 else 0.0
