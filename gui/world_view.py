"""
World view widget for displaying the game world
"""

import tkinter as tk
from tkinter import ttk
import math

try:
    from core.config import Constants
except ImportError:
    # Fallback constants if import fails
    class Constants:
        TILE_EMPTY = 0
        TILE_STONE = 1
        TILE_SOIL = 2
        TILE_WATER = 3
        TILE_MAGMA = 4

class WorldView:
    def __init__(self, parent):
        self.parent = parent
        self.world_state = None
        
        # View parameters
        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = 0
        self.zoom_level = 1.0
        self.tile_size = 8
        
        # Create the canvas
        self.canvas = tk.Canvas(parent, bg='black', width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        self.h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<B2-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-2>", self.on_drag_start)
        
        # Color mapping for tiles
        self.tile_colors = {
            Constants.TILE_EMPTY: '#000000',    # Black
            Constants.TILE_STONE: '#808080',   # Gray
            Constants.TILE_SOIL: '#8B4513',    # Brown
            Constants.TILE_WATER: '#0000FF',   # Blue
            Constants.TILE_MAGMA: '#FF4500',   # Red-orange
        }
        
        # Entity colors
        self.entity_colors = {
            'dwarf': '#FFD700',     # Gold
            'item': '#FFFFFF',      # White
            'building': '#8A2BE2',  # Blue-violet
        }
        
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def set_world_state(self, world_state):
        """Set the world state to display"""
        self.world_state = world_state
        if world_state:
            self.camera_x = world_state.size // 2
            self.camera_y = world_state.size // 2
            self.camera_z = world_state.find_surface_level(self.camera_x, self.camera_y)
        self.update_display()
        
    def update_display(self):
        """Update the display"""
        if not self.world_state:
            return
            
        self.canvas.delete("all")
        
        # Calculate visible area
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
            
        tiles_x = int(canvas_width / (self.tile_size * self.zoom_level)) + 2
        tiles_y = int(canvas_height / (self.tile_size * self.zoom_level)) + 2
        
        start_x = max(0, self.camera_x - tiles_x // 2)
        start_y = max(0, self.camera_y - tiles_y // 2)
        end_x = min(self.world_state.size, start_x + tiles_x)
        end_y = min(self.world_state.size, start_y + tiles_y)
        
        # Draw tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                self.draw_tile(x, y)
                
        # Draw entities
        self.draw_entities()
        
        # Draw UI elements
        self.draw_ui()
        
    def draw_tile(self, world_x, world_y):
        """Draw a single tile"""
        if not self.world_state.is_valid_coordinate(world_x, world_y, self.camera_z):
            return
            
        tile = self.world_state.get_tile(world_x, world_y, self.camera_z)
        
        # Calculate screen position
        screen_x = (world_x - self.camera_x) * self.tile_size * self.zoom_level + self.canvas.winfo_width() // 2
        screen_y = (world_y - self.camera_y) * self.tile_size * self.zoom_level + self.canvas.winfo_height() // 2
        
        size = self.tile_size * self.zoom_level
        
        # Get tile color
        color = self.tile_colors.get(tile.material, '#404040')
        
        # Modify color based on tile properties
        if tile.water_level > 0:
            # Water overlay
            alpha = min(tile.water_level / 7.0, 1.0)
            color = self.blend_colors(color, '#0000FF', alpha)
            
        if tile.minerals:
            # Mineral deposits
            color = self.blend_colors(color, '#FFD700', 0.3)
            
        if tile.is_designated_for_mining:
            # Mining designation
            color = self.blend_colors(color, '#FF0000', 0.2)
            
        # Draw the tile
        self.canvas.create_rectangle(
            screen_x, screen_y, screen_x + size, screen_y + size,
            fill=color, outline='', tags="tile"
        )
        
        # Draw additional indicators
        if tile.water_level > 4:
            # High water level indicator
            self.canvas.create_text(
                screen_x + size//2, screen_y + size//2,
                text="~", fill='white', font=('Arial', int(size//2)), tags="water"
            )
            
    def draw_entities(self):
        """Draw entities on the world"""
        # This would be implemented when we have access to entities
        # For now, we'll draw placeholder entities
        pass
        
    def draw_ui(self):
        """Draw UI elements"""
        # Draw coordinate display
        coord_text = f"({self.camera_x}, {self.camera_y}, {self.camera_z})"
        self.canvas.create_text(
            10, 10, text=coord_text, fill='white', anchor='nw', tags="ui"
        )
        
        # Draw zoom level
        zoom_text = f"Zoom: {self.zoom_level:.1f}x"
        self.canvas.create_text(
            10, 30, text=zoom_text, fill='white', anchor='nw', tags="ui"
        )
        
    def blend_colors(self, color1, color2, alpha):
        """Blend two colors with given alpha"""
        # Simple color blending
        try:
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 * (1 - alpha) + r2 * alpha)
            g = int(g1 * (1 - alpha) + g2 * alpha)
            b = int(b1 * (1 - alpha) + b2 * alpha)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color1
            
    def on_click(self, event):
        """Handle left mouse click"""
        world_x, world_y = self.screen_to_world(event.x, event.y)
        print(f"Clicked tile: ({world_x}, {world_y}, {self.camera_z})")
        
    def on_right_click(self, event):
        """Handle right mouse click"""
        world_x, world_y = self.screen_to_world(event.x, event.y)
        # Could show context menu here
        print(f"Right-clicked tile: ({world_x}, {world_y}, {self.camera_z})")
        
    def on_mousewheel(self, event):
        """Handle mouse wheel for zooming"""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
            
    def on_drag_start(self, event):
        """Start dragging"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
    def on_drag(self, event):
        """Handle middle mouse drag for panning"""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        # Convert screen movement to world movement
        world_dx = -dx / (self.tile_size * self.zoom_level)
        world_dy = -dy / (self.tile_size * self.zoom_level)
        
        self.move_camera(world_dx, world_dy)
        
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        world_x = self.camera_x + (screen_x - canvas_width // 2) / (self.tile_size * self.zoom_level)
        world_y = self.camera_y + (screen_y - canvas_height // 2) / (self.tile_size * self.zoom_level)
        
        return int(world_x), int(world_y)
        
    def move_camera(self, dx, dy):
        """Move the camera"""
        if not self.world_state:
            return
            
        self.camera_x = max(0, min(self.world_state.size - 1, self.camera_x + dx))
        self.camera_y = max(0, min(self.world_state.size - 1, self.camera_y + dy))
        self.update_display()
        
    def change_z_level(self, dz):
        """Change the Z level"""
        if not self.world_state:
            return
            
        self.camera_z = max(0, min(self.world_state.z_levels - 1, self.camera_z + dz))
        self.update_display()
        
    def zoom_in(self):
        """Zoom in"""
        self.zoom_level = min(4.0, self.zoom_level * 1.2)
        self.update_display()
        
    def zoom_out(self):
        """Zoom out"""
        self.zoom_level = max(0.25, self.zoom_level / 1.2)
        self.update_display()
        
    def reset_view(self):
        """Reset view to default"""
        if self.world_state:
            self.camera_x = self.world_state.size // 2
            self.camera_y = self.world_state.size // 2
            self.camera_z = self.world_state.find_surface_level(self.camera_x, self.camera_y)
        self.zoom_level = 1.0
        self.update_display()
