"""
Control panel for simulation settings and controls
"""

import tkinter as tk
from tkinter import ttk

try:
    from core.config import GameConfig
except ImportError:
    # Fallback if import fails
    class GameConfig:
        def __init__(self, **kwargs):
            self.world_size = kwargs.get('world_size', 64)
            self.z_levels = kwargs.get('z_levels', 15)
            self.initial_dwarves = kwargs.get('initial_dwarves', 7)
            self.debug_mode = kwargs.get('debug_mode', False)

class ControlPanel:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        
        # Create the main frame
        self.frame = ttk.LabelFrame(parent, text="🎛️ Controls", padding=10)
        self.frame.pack(fill=tk.X, pady=(0, 5))
        
        self.setup_world_generation()
        self.setup_simulation_controls()
        self.setup_view_controls()
        
    def setup_world_generation(self):
        """Set up world generation controls"""
        gen_frame = ttk.LabelFrame(self.frame, text="World Generation", padding=5)
        gen_frame.pack(fill=tk.X, pady=(0, 5))
        
        # World size
        ttk.Label(gen_frame, text="World Size:").grid(row=0, column=0, sticky=tk.W)
        self.world_size_var = tk.IntVar(value=64)
        world_size_combo = ttk.Combobox(gen_frame, textvariable=self.world_size_var, 
                                       values=[32, 64, 96, 128], width=10, state="readonly")
        world_size_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Z levels
        ttk.Label(gen_frame, text="Z Levels:").grid(row=1, column=0, sticky=tk.W)
        self.z_levels_var = tk.IntVar(value=15)
        z_levels_spin = ttk.Spinbox(gen_frame, from_=5, to=30, textvariable=self.z_levels_var, width=10)
        z_levels_spin.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Initial dwarves
        ttk.Label(gen_frame, text="Dwarves:").grid(row=2, column=0, sticky=tk.W)
        self.dwarves_var = tk.IntVar(value=7)
        dwarves_spin = ttk.Spinbox(gen_frame, from_=1, to=20, textvariable=self.dwarves_var, width=10)
        dwarves_spin.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        # Debug mode
        self.debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(gen_frame, text="Debug Mode", variable=self.debug_var)
        debug_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Generate button
        gen_button = ttk.Button(gen_frame, text="🌍 Generate World", 
                               command=self.main_window.new_world)
        gen_button.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)
        
    def setup_simulation_controls(self):
        """Set up simulation control buttons"""
        sim_frame = ttk.LabelFrame(self.frame, text="Simulation", padding=5)
        sim_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Control buttons
        button_frame = ttk.Frame(sim_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(button_frame, text="▶️ Start", 
                                      command=self.main_window.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=(0, 2))
        
        self.pause_button = ttk.Button(button_frame, text="⏸️ Pause", 
                                      command=self.main_window.pause_simulation)
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self.main_window.stop_simulation)
        self.stop_button.pack(side=tk.LEFT, padx=(2, 0))
        
        # Speed control
        speed_frame = ttk.Frame(sim_frame)
        speed_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=3.0, 
                               variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(side=tk.RIGHT)
        
        # Update speed label
        def update_speed_label(*args):
            self.speed_label.config(text=f"{self.speed_var.get():.1f}x")
        self.speed_var.trace('w', update_speed_label)
        
    def setup_view_controls(self):
        """Set up view control buttons"""
        view_frame = ttk.LabelFrame(self.frame, text="View", padding=5)
        view_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Camera controls
        cam_frame = ttk.Frame(view_frame)
        cam_frame.pack(fill=tk.X)
        
        # Movement buttons
        move_frame = ttk.Frame(cam_frame)
        move_frame.pack()
        
        ttk.Button(move_frame, text="↑", width=3, 
                  command=lambda: self.move_camera(0, -1)).grid(row=0, column=1)
        ttk.Button(move_frame, text="←", width=3, 
                  command=lambda: self.move_camera(-1, 0)).grid(row=1, column=0)
        ttk.Button(move_frame, text="→", width=3, 
                  command=lambda: self.move_camera(1, 0)).grid(row=1, column=2)
        ttk.Button(move_frame, text="↓", width=3, 
                  command=lambda: self.move_camera(0, 1)).grid(row=2, column=1)
        
        # Z-level controls
        z_frame = ttk.Frame(view_frame)
        z_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(z_frame, text="🔼 Up", 
                  command=lambda: self.change_z_level(1)).pack(side=tk.LEFT)
        ttk.Button(z_frame, text="🔽 Down", 
                  command=lambda: self.change_z_level(-1)).pack(side=tk.RIGHT)
        
        # Zoom controls
        zoom_frame = ttk.Frame(view_frame)
        zoom_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(zoom_frame, text="🔍+ Zoom In", 
                  command=self.main_window.zoom_in).pack(side=tk.LEFT)
        ttk.Button(zoom_frame, text="🔍- Zoom Out", 
                  command=self.main_window.zoom_out).pack(side=tk.RIGHT)
        
        # Reset view
        ttk.Button(view_frame, text="🎯 Reset View", 
                  command=self.main_window.reset_view).pack(fill=tk.X, pady=(5, 0))
        
    def move_camera(self, dx, dy):
        """Move camera by given offset"""
        if hasattr(self.main_window, 'world_view'):
            self.main_window.world_view.move_camera(dx * 5, dy * 5)
            
    def change_z_level(self, dz):
        """Change Z level"""
        if hasattr(self.main_window, 'world_view'):
            self.main_window.world_view.change_z_level(dz)
            
    def get_config(self):
        """Get current configuration from controls"""
        return GameConfig(
            world_size=self.world_size_var.get(),
            z_levels=self.z_levels_var.get(),
            initial_dwarves=self.dwarves_var.get(),
            debug_mode=self.debug_var.get()
        )
