"""
Game configuration and constants
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass
class GameConfig:
    """Main game configuration"""
    # Display settings
    debug_mode: bool = False
    ascii_mode: bool = False
    window_width: int = 1024
    window_height: int = 768
    
    # World generation
    world_size: int = 128
    z_levels: int = 20
    noise_seed: int = 42
    
    # Simulation settings
    initial_dwarves: int = 10
    max_agents: int = 100
    target_fps: int = 60
    max_memory_mb: int = 2048
    
    # Performance settings
    spatial_grid_size: int = 64
    pathfinding_cache_size: int = 1000
    update_frequency_hz: int = 10
    
    # AI settings
    ai_decision_interval: float = 0.5
    pathfinding_max_iterations: int = 1000
    relationship_update_interval: float = 2.0
    
    # Resource settings
    food_decay_rate: float = 0.01
    temperature_update_rate: float = 0.1
    fluid_simulation_steps: int = 5
    
    # Debug settings
    show_pathfinding: bool = False
    show_ai_decisions: bool = False
    show_resource_flows: bool = False
    show_performance_stats: bool = False

# Game constants
class Constants:
    # Tile types
    TILE_EMPTY = 0
    TILE_STONE = 1
    TILE_SOIL = 2
    TILE_WATER = 3
    TILE_MAGMA = 4
    
    # Material types
    MATERIAL_STONE = "stone"
    MATERIAL_METAL = "metal"
    MATERIAL_WOOD = "wood"
    MATERIAL_FOOD = "food"
    
    # Dwarf needs
    NEED_FOOD = "food"
    NEED_DRINK = "drink"
    NEED_SLEEP = "sleep"
    NEED_SOCIAL = "social"
    NEED_WORK = "work"
    
    # Skills
    SKILL_MINING = "mining"
    SKILL_CRAFTING = "crafting"
    SKILL_COMBAT = "combat"
    SKILL_FARMING = "farming"
    
    # Biome types
    BIOME_MOUNTAIN = "mountain"
    BIOME_FOREST = "forest"
    BIOME_DESERT = "desert"
    BIOME_SWAMP = "swamp"
    
    # Water levels (0-7)
    WATER_LEVELS = 8
    
    # Temperature ranges
    TEMP_FREEZING = 0
    TEMP_COLD = 10
    TEMP_NORMAL = 20
    TEMP_HOT = 30
    TEMP_MAGMA = 100
