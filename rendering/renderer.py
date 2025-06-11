"""
Rendering system with ASCII fallback mode
"""

import sys
import os
from typing import List, Dict, Any, Optional, Tuple
from core.config import GameConfig, Constants
from world.world_state import WorldState

class Renderer:
    def __init__(self, config: GameConfig, world_state: WorldState):
        self.config = config
        self.world_state = world_state
        
        # Rendering state
        self.camera_x = world_state.size // 2
        self.camera_y = world_state.size // 2
        self.camera_z = world_state.find_surface_level(self.camera_x, self.camera_y)
        self.zoom_level = 1.0
        
        # View dimensions
        self.view_width = 80
        self.view_height = 24
        
        # ASCII character mappings
        self.tile_chars = {
            Constants.TILE_EMPTY: ' ',
            Constants.TILE_STONE: '#',
            Constants.TILE_SOIL: '.',
            Constants.TILE_WATER: '~',
            Constants.TILE_MAGMA: '*'
        }
        
        # Entity character mappings
        self.entity_chars = {
            'dwarf': '@',
            'item': '%',
            'building': '&'
        }
        
        # Color support (if available)
        self.colors_available = self._init_colors()
        
        # Frame buffer for ASCII rendering
        self.frame_buffer = []
        self.debug_lines = []
        
    def _init_colors(self) -> bool:
        """Initialize color support if available"""
        try:
            import colorama
            colorama.init()
            return True
        except ImportError:
            return False
            
    def render(self, entities: List[Any], debug_info: Optional[Dict[str, Any]] = None):
        """Render the current game state"""
        if self.config.ascii_mode:
            self._render_ascii(entities, debug_info)
        else:
            self._render_ascii(entities, debug_info)  # For now, always use ASCII
            
    def _render_ascii(self, entities: List[Any], debug_info: Optional[Dict[str, Any]] = None):
        """Render using ASCII characters"""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Initialize frame buffer
        self.frame_buffer = [[' ' for _ in range(self.view_width)] for _ in range(self.view_height)]
        
        # Render world tiles
        self._render_world_ascii()
        
        # Render entities
        self._render_entities_ascii(entities)
        
        # Render debug overlays
        if debug_info:
            self._render_debug_overlays_ascii(debug_info)
            
        # Output frame buffer
        self._output_frame_buffer()
        
        # Render UI
        self._render_ui_ascii(debug_info)
        
    def _render_world_ascii(self):
        """Render world tiles in ASCII"""
        start_x = max(0, self.camera_x - self.view_width // 2)
        start_y = max(0, self.camera_y - self.view_height // 2)
        
        for screen_y in range(self.view_height):
            for screen_x in range(self.view_width):
                world_x = start_x + screen_x
                world_y = start_y + screen_y
                
                if (world_x < self.world_state.size and 
                    world_y < self.world_state.size):
                    
                    tile = self.world_state.get_tile(world_x, world_y, self.camera_z)
                    char = self.tile_chars.get(tile.material, '?')
                    
                    # Modify character based on tile properties
                    if tile.water_level > 0:
                        char = '~' if tile.water_level < 7 else '≈'
                    elif tile.is_designated_for_mining:
                        char = 'x'
                    elif tile.minerals:
                        char = '$'
                        
                    self.frame_buffer[screen_y][screen_x] = char
                    
    def _render_entities_ascii(self, entities: List[Any]):
        """Render entities in ASCII"""
        start_x = max(0, self.camera_x - self.view_width // 2)
        start_y = max(0, self.camera_y - self.view_height // 2)
        
        for entity in entities:
            if hasattr(entity, 'position'):
                world_x, world_y, world_z = entity.position
                
                # Only render entities on current z-level
                if world_z != self.camera_z:
                    continue
                    
                # Convert to screen coordinates
                screen_x = world_x - start_x
                screen_y = world_y - start_y
                
                if (0 <= screen_x < self.view_width and 
                    0 <= screen_y < self.view_height):
                    
                    entity_type = getattr(entity, 'entity_type', 'unknown')
                    char = self.entity_chars.get(entity_type, '?')
                    
                    self.frame_buffer[screen_y][screen_x] = char
                    
    def _render_debug_overlays_ascii(self, debug_info: Dict[str, Any]):
        """Render debug overlays in ASCII"""
        if self.config.show_pathfinding and 'pathfinding_data' in debug_info:
            self._render_pathfinding_debug(debug_info['pathfinding_data'])
            
    def _render_pathfinding_debug(self, pathfinding_data: Dict[str, Any]):
        """Render pathfinding debug information"""
        start_x = max(0, self.camera_x - self.view_width // 2)
        start_y = max(0, self.camera_y - self.view_height // 2)
        
        for entity_id, data in pathfinding_data.items():
            if 'path' in data and data['path']:
                for i, (world_x, world_y, world_z) in enumerate(data['path']):
                    if world_z != self.camera_z:
                        continue
                        
                    screen_x = world_x - start_x
                    screen_y = world_y - start_y
                    
                    if (0 <= screen_x < self.view_width and 
                        0 <= screen_y < self.view_height):
                        
                        if i == 0:
                            char = 'S'  # Start
                        elif i == len(data['path']) - 1:
                            char = 'G'  # Goal
                        else:
                            char = '·'  # Path
                            
                        self.frame_buffer[screen_y][screen_x] = char
                        
    def _output_frame_buffer(self):
        """Output the frame buffer to console"""
        for row in self.frame_buffer:
            print(''.join(row))
            
    def _render_ui_ascii(self, debug_info: Optional[Dict[str, Any]] = None):
        """Render UI elements in ASCII"""
        # Status line
        status_line = f"Pos: ({self.camera_x}, {self.camera_y}, {self.camera_z}) | "
        
        if debug_info:
            status_line += f"FPS: {debug_info.get('fps', 0)} | "
            status_line += f"Entities: {debug_info.get('entity_count', 0)} | "
            status_line += f"Memory: {debug_info.get('memory_usage', 0):.1f}MB"
            
        print("=" * self.view_width)
        print(status_line[:self.view_width])
        
        # Debug information
        if debug_info and self.config.show_ai_decisions:
            print("\nAI Decisions:")
            ai_data = debug_info.get('ai_decisions', {})
            for entity_id, data in list(ai_data.items())[:5]:  # Show first 5
                decision = data.get('current_decision', 'None')
                mood = data.get('mood', 0)
                print(f"  Entity {entity_id}: {decision} (mood: {mood:.1f})")
                
        if debug_info and self.config.show_resource_flows:
            print("\nResource Flows:")
            flow_data = debug_info.get('resource_flows', {})
            for flow_key, data in list(flow_data.items())[:3]:  # Show first 3
                item_type = data.get('item_type', 'unknown')
                amount = data.get('amount_moved', 0)
                print(f"  {flow_key}: {amount} {item_type}")
                
        # Controls
        print("\nControls: WASD=move camera, QE=change z-level, R=reset view, ESC=quit")
        
    def move_camera(self, dx: int, dy: int, dz: int = 0):
        """Move camera position"""
        self.camera_x = max(0, min(self.world_state.size - 1, self.camera_x + dx))
        self.camera_y = max(0, min(self.world_state.size - 1, self.camera_y + dy))
        self.camera_z = max(0, min(self.world_state.z_levels - 1, self.camera_z + dz))
        
    def center_camera_on(self, x: int, y: int, z: int):
        """Center camera on specific coordinates"""
        self.camera_x = max(0, min(self.world_state.size - 1, x))
        self.camera_y = max(0, min(self.world_state.size - 1, y))
        self.camera_z = max(0, min(self.world_state.z_levels - 1, z))
        
    def update_interpolation(self, dt: float):
        """Update rendering interpolation for smooth movement"""
        # For ASCII rendering, no interpolation needed
        pass
        
    def reinitialize(self, world_state: WorldState):
        """Reinitialize renderer with new world state"""
        self.world_state = world_state
        self.camera_x = world_state.size // 2
        self.camera_y = world_state.size // 2
        self.camera_z = world_state.find_surface_level(self.camera_x, self.camera_y)
        
    def get_screen_coordinates(self, world_pos: Tuple[int, int, int]) -> Optional[Tuple[int, int]]:
        """Convert world coordinates to screen coordinates"""
        world_x, world_y, world_z = world_pos
        
        if world_z != self.camera_z:
            return None
            
        start_x = max(0, self.camera_x - self.view_width // 2)
        start_y = max(0, self.camera_y - self.view_height // 2)
        
        screen_x = world_x - start_x
        screen_y = world_y - start_y
        
        if (0 <= screen_x < self.view_width and 
            0 <= screen_y < self.view_height):
            return (screen_x, screen_y)
            
        return None
        
    def get_world_coordinates(self, screen_pos: Tuple[int, int]) -> Tuple[int, int, int]:
        """Convert screen coordinates to world coordinates"""
        screen_x, screen_y = screen_pos
        
        start_x = max(0, self.camera_x - self.view_width // 2)
        start_y = max(0, self.camera_y - self.view_height // 2)
        
        world_x = start_x + screen_x
        world_y = start_y + screen_y
        
        return (world_x, world_y, self.camera_z)
