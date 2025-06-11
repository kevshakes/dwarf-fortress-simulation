"""
Game engine optimized for GUI with graceful dependency handling
"""

import time
import sys
import os
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import with fallbacks
try:
    from core.config import GameConfig
    from world.world_generator import WorldGenerator
    from world.world_state_simple import WorldState
    from entities.entity_manager import EntityManager
    from ai.ai_manager import AIManager
    from resources.resource_manager import ResourceManager
    from simulation.physics_engine import PhysicsEngine
    from utils.spatial_partition import SpatialPartition
    from utils.save_system import SaveSystem
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Import warning: {e}")
    print("Some features may be limited. Please check your installation.")
    IMPORTS_AVAILABLE = False
    
    # Minimal fallback classes
    class GameConfig:
        def __init__(self, **kwargs):
            self.world_size = kwargs.get('world_size', 64)
            self.z_levels = kwargs.get('z_levels', 15)
            self.initial_dwarves = kwargs.get('initial_dwarves', 7)
            self.debug_mode = kwargs.get('debug_mode', False)
            self.show_pathfinding = False
            self.show_ai_decisions = False
            self.show_resource_flows = False

# Memory usage fallback
try:
    import psutil
    import os
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
except ImportError:
    def get_memory_usage():
        return 0.0

class GameEngineGUI:
    """Game engine optimized for GUI usage with dependency fallbacks"""
    
    def __init__(self, config):
        self.config = config
        self.world_state = None
        self.entity_manager = None
        self.ai_manager = None
        self.resource_manager = None
        self.physics_engine = None
        self.spatial_partition = None
        self.save_system = None
        
        # Timing
        self.last_update_time = 0
        self.accumulated_time = 0
        self.fixed_timestep = 1.0 / 10  # 10 Hz for GUI
        
        # Performance tracking
        self.frame_count = 0
        self.last_fps_time = 0
        self.current_fps = 0
        
        # Initialize save system
        if IMPORTS_AVAILABLE:
            self.save_system = SaveSystem()
        
    def initialize(self):
        """Initialize all game systems with fallbacks"""
        if not IMPORTS_AVAILABLE:
            # Create minimal world state for GUI testing
            self.world_state = self._create_minimal_world()
            return
            
        try:
            print("Generating world...")
            world_generator = WorldGenerator(self.config)
            self.world_state = world_generator.generate()
            
            print("Initializing spatial partitioning...")
            self.spatial_partition = SpatialPartition(
                self.config.world_size, 
                64  # Fixed grid size for GUI
            )
            
            print("Initializing entity manager...")
            self.entity_manager = EntityManager(self.config, self.world_state)
            
            print("Initializing AI manager...")
            self.ai_manager = AIManager(self.config, self.world_state, self.entity_manager)
            
            print("Initializing resource manager...")
            self.resource_manager = ResourceManager(self.config, self.world_state)
            
            print("Initializing physics engine...")
            self.physics_engine = PhysicsEngine(self.config, self.world_state)
            
            # Create initial dwarves
            print(f"Creating {self.config.initial_dwarves} dwarves...")
            self.entity_manager.create_initial_dwarves(self.config.initial_dwarves)
            
            self.last_update_time = time.time()
            print("Game engine initialized successfully!")
            
        except Exception as e:
            print(f"Initialization error: {e}")
            # Fall back to minimal world
            self.world_state = self._create_minimal_world()
            
    def _create_minimal_world(self):
        """Create a minimal world state for testing"""
        from world.world_state_simple import WorldState, Tile
        from core.config import Constants
        
        world = WorldState(self.config.world_size, self.config.z_levels)
        
        # Create some basic terrain
        for x in range(world.size):
            for y in range(world.size):
                for z in range(world.z_levels):
                    tile = world.get_tile(x, y, z)
                    
                    # Simple terrain generation
                    if z < world.z_levels // 3:
                        tile.material = Constants.TILE_STONE
                    elif z < world.z_levels * 2 // 3:
                        tile.material = Constants.TILE_SOIL
                    else:
                        tile.material = Constants.TILE_EMPTY
                        
                    world.set_tile(x, y, z, tile)
        
        return world
        
    def update(self, delta_time: float):
        """Update all game systems with delta time"""
        if not IMPORTS_AVAILABLE:
            # Minimal update for GUI testing
            self.update_fps_counter()
            return
            
        self.accumulated_time += delta_time
        
        # Fixed timestep updates for simulation stability
        while self.accumulated_time >= self.fixed_timestep:
            self.fixed_update(self.fixed_timestep)
            self.accumulated_time -= self.fixed_timestep
            
        # Update FPS counter
        self.update_fps_counter()
        
    def fixed_update(self, dt: float):
        """Fixed timestep update for simulation systems"""
        try:
            # Update spatial partitioning
            if self.spatial_partition and self.entity_manager:
                self.spatial_partition.update(self.entity_manager.get_all_entities())
            
            # Update AI decisions
            if self.ai_manager:
                self.ai_manager.update(dt)
            
            # Update physics simulation
            if self.physics_engine:
                self.physics_engine.update(dt)
            
            # Update resource management
            if self.resource_manager:
                self.resource_manager.update(dt)
            
            # Update entities
            if self.entity_manager:
                self.entity_manager.update(dt)
                
        except Exception as e:
            print(f"Update error: {e}")
            
    def get_debug_info(self) -> Dict[str, Any]:
        """Collect debug information from all systems"""
        debug_info = {
            'fps': self.current_fps,
            'entity_count': self.get_entity_count(),
            'memory_usage': self.get_memory_usage(),
        }
        
        if not IMPORTS_AVAILABLE:
            return debug_info
            
        try:
            if self.ai_manager:
                debug_info['pathfinding_cache_size'] = self.ai_manager.get_pathfinding_cache_size()
                
                if self.config.show_pathfinding:
                    debug_info['pathfinding_data'] = self.ai_manager.get_pathfinding_debug_data()
                    
                if self.config.show_ai_decisions:
                    debug_info['ai_decisions'] = self.ai_manager.get_decision_debug_data()
                    
            if self.resource_manager and self.config.show_resource_flows:
                debug_info['resource_flows'] = self.resource_manager.get_flow_debug_data()
                
        except Exception as e:
            print(f"Debug info error: {e}")
            
        return debug_info
        
    def update_fps_counter(self):
        """Update FPS counter"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_fps_time = current_time
            
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        return get_memory_usage()
        
    def get_entity_count(self) -> int:
        """Get total entity count"""
        if self.entity_manager:
            return self.entity_manager.get_entity_count()
        return 0
        
    def save_game(self, filename: str):
        """Save current game state"""
        if not self.save_system or not IMPORTS_AVAILABLE:
            print("Save system not available")
            return
            
        try:
            game_state = {
                'world_state': self.world_state,
                'entities': self.entity_manager.serialize() if self.entity_manager else {},
                'resources': self.resource_manager.serialize() if self.resource_manager else {},
                'config': self.config
            }
            self.save_system.save(game_state, filename)
            print(f"Game saved to {filename}")
            
        except Exception as e:
            print(f"Save error: {e}")
            
    def load_game(self, filename: str):
        """Load game state from file"""
        if not self.save_system or not IMPORTS_AVAILABLE:
            print("Save system not available")
            return
            
        try:
            game_state = self.save_system.load(filename)
            
            self.world_state = game_state['world_state']
            
            if self.entity_manager:
                self.entity_manager.deserialize(game_state['entities'])
            if self.resource_manager:
                self.resource_manager.deserialize(game_state['resources'])
            
            # Reinitialize systems that depend on loaded state
            if self.ai_manager:
                self.ai_manager.reinitialize(self.world_state, self.entity_manager)
            if self.physics_engine:
                self.physics_engine.reinitialize(self.world_state)
                
            print(f"Game loaded from {filename}")
            
        except Exception as e:
            print(f"Load error: {e}")

# Alias for compatibility
GameEngine = GameEngineGUI
