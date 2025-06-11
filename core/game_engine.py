"""
Main game engine coordinating all systems
"""

import time
from typing import Dict, List, Any
from core.config import GameConfig
from world.world_generator import WorldGenerator
from world.world_state import WorldState
from entities.entity_manager import EntityManager
from ai.ai_manager import AIManager
from resources.resource_manager import ResourceManager
from simulation.physics_engine import PhysicsEngine
from rendering.renderer import Renderer
from utils.spatial_partition import SpatialPartition
from utils.save_system import SaveSystem

class GameEngine:
    def __init__(self, config: GameConfig):
        self.config = config
        self.world_state = None
        self.entity_manager = None
        self.ai_manager = None
        self.resource_manager = None
        self.physics_engine = None
        self.renderer = None
        self.spatial_partition = None
        self.save_system = SaveSystem()
        
        # Timing
        self.last_update_time = 0
        self.accumulated_time = 0
        self.fixed_timestep = 1.0 / config.update_frequency_hz
        
        # Performance tracking
        self.frame_count = 0
        self.last_fps_time = 0
        self.current_fps = 0
        
    def initialize(self):
        """Initialize all game systems"""
        print("Generating world...")
        world_generator = WorldGenerator(self.config)
        self.world_state = world_generator.generate()
        
        print("Initializing spatial partitioning...")
        self.spatial_partition = SpatialPartition(
            self.config.world_size, 
            self.config.spatial_grid_size
        )
        
        print("Initializing entity manager...")
        self.entity_manager = EntityManager(self.config, self.world_state)
        
        print("Initializing AI manager...")
        self.ai_manager = AIManager(self.config, self.world_state, self.entity_manager)
        
        print("Initializing resource manager...")
        self.resource_manager = ResourceManager(self.config, self.world_state)
        
        print("Initializing physics engine...")
        self.physics_engine = PhysicsEngine(self.config, self.world_state)
        
        print("Initializing renderer...")
        self.renderer = Renderer(self.config, self.world_state)
        
        # Create initial dwarves
        print(f"Creating {self.config.initial_dwarves} dwarves...")
        self.entity_manager.create_initial_dwarves(self.config.initial_dwarves)
        
        self.last_update_time = time.time()
        
    def update(self, delta_time: float):
        """Update all game systems with delta time"""
        self.accumulated_time += delta_time
        
        # Fixed timestep updates for simulation stability
        while self.accumulated_time >= self.fixed_timestep:
            self.fixed_update(self.fixed_timestep)
            self.accumulated_time -= self.fixed_timestep
            
        # Variable timestep updates for smooth rendering
        self.variable_update(delta_time)
        
        # Update FPS counter
        self.update_fps_counter()
        
    def fixed_update(self, dt: float):
        """Fixed timestep update for simulation systems"""
        # Update spatial partitioning
        self.spatial_partition.update(self.entity_manager.get_all_entities())
        
        # Update AI decisions
        self.ai_manager.update(dt)
        
        # Update physics simulation
        self.physics_engine.update(dt)
        
        # Update resource management
        self.resource_manager.update(dt)
        
        # Update entities
        self.entity_manager.update(dt)
        
    def variable_update(self, dt: float):
        """Variable timestep update for rendering and UI"""
        # Update renderer interpolation
        self.renderer.update_interpolation(dt)
        
    def render(self):
        """Render the current game state"""
        self.renderer.render(
            entities=self.entity_manager.get_visible_entities(),
            debug_info=self.get_debug_info() if self.config.debug_mode else None
        )
        
    def get_debug_info(self) -> Dict[str, Any]:
        """Collect debug information from all systems"""
        debug_info = {
            'fps': self.current_fps,
            'entity_count': self.entity_manager.get_entity_count(),
            'memory_usage': self.get_memory_usage(),
            'pathfinding_cache_size': self.ai_manager.get_pathfinding_cache_size(),
        }
        
        if self.config.show_pathfinding:
            debug_info['pathfinding_data'] = self.ai_manager.get_pathfinding_debug_data()
            
        if self.config.show_ai_decisions:
            debug_info['ai_decisions'] = self.ai_manager.get_decision_debug_data()
            
        if self.config.show_resource_flows:
            debug_info['resource_flows'] = self.resource_manager.get_flow_debug_data()
            
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
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
        
    def save_game(self, filename: str):
        """Save current game state"""
        game_state = {
            'world_state': self.world_state,
            'entities': self.entity_manager.serialize(),
            'resources': self.resource_manager.serialize(),
            'config': self.config
        }
        self.save_system.save(game_state, filename)
        
    def load_game(self, filename: str):
        """Load game state from file"""
        game_state = self.save_system.load(filename)
        
        self.world_state = game_state['world_state']
        self.entity_manager.deserialize(game_state['entities'])
        self.resource_manager.deserialize(game_state['resources'])
        
        # Reinitialize systems that depend on loaded state
        self.ai_manager.reinitialize(self.world_state, self.entity_manager)
        self.physics_engine.reinitialize(self.world_state)
        self.renderer.reinitialize(self.world_state)
