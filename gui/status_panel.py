"""
Status panel showing game statistics and information
"""

import tkinter as tk
from tkinter import ttk

class StatusPanel:
    def __init__(self, parent):
        self.parent = parent
        self.game_engine = None
        
        # Create the main frame
        self.frame = ttk.LabelFrame(parent, text="📊 Status", padding=10)
        self.frame.pack(fill=tk.X, pady=(0, 5))
        
        self.setup_status_display()
        
    def setup_status_display(self):
        """Set up the status display"""
        # Performance stats
        perf_frame = ttk.LabelFrame(self.frame, text="Performance", padding=5)
        perf_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.fps_label = ttk.Label(perf_frame, text="FPS: --")
        self.fps_label.pack(anchor=tk.W)
        
        self.memory_label = ttk.Label(perf_frame, text="Memory: -- MB")
        self.memory_label.pack(anchor=tk.W)
        
        # World stats
        world_frame = ttk.LabelFrame(self.frame, text="World", padding=5)
        world_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.world_size_label = ttk.Label(world_frame, text="Size: --")
        self.world_size_label.pack(anchor=tk.W)
        
        self.z_levels_label = ttk.Label(world_frame, text="Z-Levels: --")
        self.z_levels_label.pack(anchor=tk.W)
        
        self.year_label = ttk.Label(world_frame, text="Year: --")
        self.year_label.pack(anchor=tk.W)
        
        # Population stats
        pop_frame = ttk.LabelFrame(self.frame, text="Population", padding=5)
        pop_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.dwarves_label = ttk.Label(pop_frame, text="Dwarves: --")
        self.dwarves_label.pack(anchor=tk.W)
        
        self.entities_label = ttk.Label(pop_frame, text="Total Entities: --")
        self.entities_label.pack(anchor=tk.W)
        
        # Resource stats
        res_frame = ttk.LabelFrame(self.frame, text="Resources", padding=5)
        res_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.stockpiles_label = ttk.Label(res_frame, text="Stockpiles: --")
        self.stockpiles_label.pack(anchor=tk.W)
        
        self.production_label = ttk.Label(res_frame, text="Production: --")
        self.production_label.pack(anchor=tk.W)
        
    def set_game_engine(self, game_engine):
        """Set the game engine to monitor"""
        self.game_engine = game_engine
        self.update_display()
        
    def update_display(self):
        """Update the status display"""
        if not self.game_engine:
            return
            
        try:
            # Performance stats
            fps = getattr(self.game_engine, 'current_fps', 0)
            self.fps_label.config(text=f"FPS: {fps:.1f}")
            
            memory = self.game_engine.get_memory_usage()
            self.memory_label.config(text=f"Memory: {memory:.1f} MB")
            
            # World stats
            world_state = self.game_engine.world_state
            if world_state:
                self.world_size_label.config(text=f"Size: {world_state.size}x{world_state.size}")
                self.z_levels_label.config(text=f"Z-Levels: {world_state.z_levels}")
                self.year_label.config(text=f"Year: {world_state.current_year}")
                
            # Population stats
            entity_manager = self.game_engine.entity_manager
            if entity_manager:
                dwarves = len(entity_manager.get_entities_by_type('dwarf'))
                total_entities = entity_manager.get_entity_count()
                
                self.dwarves_label.config(text=f"Dwarves: {dwarves}")
                self.entities_label.config(text=f"Total Entities: {total_entities}")
                
            # Resource stats
            resource_manager = self.game_engine.resource_manager
            if resource_manager:
                stockpiles = len(resource_manager.stockpile_manager.get_all_stockpiles())
                production_status = resource_manager.get_production_status()
                production_queue = production_status.get('queue_length', 0)
                
                self.stockpiles_label.config(text=f"Stockpiles: {stockpiles}")
                self.production_label.config(text=f"Production Queue: {production_queue}")
                
        except Exception as e:
            print(f"Status update error: {e}")

class DebugPanel:
    def __init__(self, parent):
        self.parent = parent
        self.game_engine = None
        self.visible = False
        
        # Create the main frame (initially hidden)
        self.frame = ttk.LabelFrame(parent, text="🔧 Debug", padding=10)
        
        self.setup_debug_display()
        
    def setup_debug_display(self):
        """Set up the debug display"""
        # Debug controls
        controls_frame = ttk.Frame(self.frame)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.pathfinding_var = tk.BooleanVar()
        ttk.Checkbutton(controls_frame, text="Show Pathfinding", 
                       variable=self.pathfinding_var,
                       command=self.toggle_pathfinding).pack(anchor=tk.W)
        
        self.ai_decisions_var = tk.BooleanVar()
        ttk.Checkbutton(controls_frame, text="Show AI Decisions", 
                       variable=self.ai_decisions_var,
                       command=self.toggle_ai_decisions).pack(anchor=tk.W)
        
        self.resource_flows_var = tk.BooleanVar()
        ttk.Checkbutton(controls_frame, text="Show Resource Flows", 
                       variable=self.resource_flows_var,
                       command=self.toggle_resource_flows).pack(anchor=tk.W)
        
        # Debug info display
        info_frame = ttk.LabelFrame(self.frame, text="Debug Info", padding=5)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget for debug output
        self.debug_text = tk.Text(info_frame, height=10, width=30, font=('Courier', 8))
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.debug_text.yview)
        self.debug_text.configure(yscrollcommand=scrollbar.set)
        
        self.debug_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def set_game_engine(self, game_engine):
        """Set the game engine to monitor"""
        self.game_engine = game_engine
        
    def toggle_visibility(self):
        """Toggle debug panel visibility"""
        if self.visible:
            self.frame.pack_forget()
            self.visible = False
        else:
            self.frame.pack(fill=tk.BOTH, expand=True)
            self.visible = True
            
    def toggle_pathfinding(self):
        """Toggle pathfinding debug display"""
        if self.game_engine and hasattr(self.game_engine, 'config'):
            self.game_engine.config.show_pathfinding = self.pathfinding_var.get()
            
    def toggle_ai_decisions(self):
        """Toggle AI decisions debug display"""
        if self.game_engine and hasattr(self.game_engine, 'config'):
            self.game_engine.config.show_ai_decisions = self.ai_decisions_var.get()
            
    def toggle_resource_flows(self):
        """Toggle resource flows debug display"""
        if self.game_engine and hasattr(self.game_engine, 'config'):
            self.game_engine.config.show_resource_flows = self.resource_flows_var.get()
            
    def update_display(self):
        """Update the debug display"""
        if not self.visible or not self.game_engine:
            return
            
        try:
            debug_info = self.game_engine.get_debug_info()
            if debug_info:
                # Clear previous content
                self.debug_text.delete(1.0, tk.END)
                
                # Add debug information
                debug_lines = []
                
                if 'pathfinding_data' in debug_info:
                    debug_lines.append("=== PATHFINDING ===")
                    for entity_id, data in debug_info['pathfinding_data'].items():
                        path_len = data.get('path_length', 0)
                        debug_lines.append(f"Entity {entity_id}: path length {path_len}")
                        
                if 'ai_decisions' in debug_info:
                    debug_lines.append("\n=== AI DECISIONS ===")
                    for entity_id, data in debug_info['ai_decisions'].items():
                        decision = data.get('current_decision', 'None')
                        mood = data.get('mood', 0)
                        debug_lines.append(f"Entity {entity_id}: {decision} (mood: {mood:.2f})")
                        
                if 'resource_flows' in debug_info:
                    debug_lines.append("\n=== RESOURCE FLOWS ===")
                    for flow_key, data in debug_info['resource_flows'].items():
                        item_type = data.get('item_type', 'unknown')
                        amount = data.get('amount_moved', 0)
                        debug_lines.append(f"{flow_key}: {amount} {item_type}")
                
                # Insert debug text
                debug_text = '\n'.join(debug_lines)
                self.debug_text.insert(tk.END, debug_text)
                
                # Auto-scroll to bottom
                self.debug_text.see(tk.END)
                
        except Exception as e:
            print(f"Debug update error: {e}")
