"""
Main GUI window for the Dwarf Fortress Simulation
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.config import GameConfig, Constants
    from core.game_engine_gui import GameEngineGUI as GameEngine
    from gui.world_view import WorldView
    from gui.control_panel import ControlPanel
    from gui.status_panel import StatusPanel, DebugPanel
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏰 Dwarf Fortress Simulation")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Game state
        self.game_engine = None
        self.game_thread = None
        self.running = False
        self.paused = False
        
        # Create GUI components
        self.setup_gui()
        self.setup_menu()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_gui(self):
        """Set up the main GUI layout"""
        # Create main frames
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for world view
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right panel for controls
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # World view (main display)
        self.world_view = WorldView(self.left_frame)
        
        # Control panels
        self.control_panel = ControlPanel(self.right_frame, self)
        self.status_panel = StatusPanel(self.right_frame)
        self.debug_panel = DebugPanel(self.right_frame)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready to start simulation", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_menu(self):
        """Set up the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New World", command=self.new_world)
        file_menu.add_command(label="Load World", command=self.load_world)
        file_menu.add_command(label="Save World", command=self.save_world)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Simulation menu
        sim_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Simulation", menu=sim_menu)
        sim_menu.add_command(label="Start", command=self.start_simulation)
        sim_menu.add_command(label="Pause", command=self.pause_simulation)
        sim_menu.add_command(label="Stop", command=self.stop_simulation)
        sim_menu.add_separator()
        sim_menu.add_command(label="Speed Up", command=self.speed_up)
        sim_menu.add_command(label="Slow Down", command=self.slow_down)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        view_menu.add_command(label="Reset View", command=self.reset_view)
        view_menu.add_separator()
        view_menu.add_command(label="Show Debug Info", command=self.toggle_debug)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Controls", command=self.show_controls)
        help_menu.add_command(label="About", command=self.show_about)
        
    def new_world(self):
        """Create a new world"""
        if self.running:
            messagebox.showwarning("Warning", "Please stop the current simulation first.")
            return
            
        try:
            # Get world parameters from control panel
            config = self.control_panel.get_config()
            
            self.update_status("Generating new world...")
            self.root.update()
            
            # Create game engine
            self.game_engine = GameEngine(config)
            self.game_engine.initialize()
            
            # Update displays
            self.world_view.set_world_state(self.game_engine.world_state)
            self.status_panel.set_game_engine(self.game_engine)
            self.debug_panel.set_game_engine(self.game_engine)
            
            self.update_status("World generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate world: {e}")
            self.update_status("World generation failed")
            
    def load_world(self):
        """Load a saved world"""
        from tkinter import filedialog
        
        if self.running:
            messagebox.showwarning("Warning", "Please stop the current simulation first.")
            return
            
        filename = filedialog.askopenfilename(
            title="Load World",
            filetypes=[("Save files", "*.dat"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                config = GameConfig()
                self.game_engine = GameEngine(config)
                self.game_engine.load_game(filename)
                
                self.world_view.set_world_state(self.game_engine.world_state)
                self.status_panel.set_game_engine(self.game_engine)
                self.debug_panel.set_game_engine(self.game_engine)
                
                self.update_status(f"World loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load world: {e}")
                
    def save_world(self):
        """Save the current world"""
        from tkinter import filedialog
        
        if not self.game_engine:
            messagebox.showwarning("Warning", "No world to save.")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save World",
            defaultextension=".dat",
            filetypes=[("Save files", "*.dat"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.game_engine.save_game(filename)
                self.update_status(f"World saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save world: {e}")
                
    def start_simulation(self):
        """Start the simulation"""
        if not self.game_engine:
            messagebox.showwarning("Warning", "Please create or load a world first.")
            return
            
        if self.running:
            return
            
        self.running = True
        self.paused = False
        self.game_thread = threading.Thread(target=self.game_loop, daemon=True)
        self.game_thread.start()
        
        self.update_status("Simulation started")
        
    def pause_simulation(self):
        """Pause/unpause the simulation"""
        if not self.running:
            return
            
        self.paused = not self.paused
        status = "paused" if self.paused else "resumed"
        self.update_status(f"Simulation {status}")
        
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        if self.game_thread:
            self.game_thread.join(timeout=1.0)
        self.update_status("Simulation stopped")
        
    def game_loop(self):
        """Main game loop running in separate thread"""
        last_time = time.time()
        target_fps = 30  # GUI update rate
        frame_time = 1.0 / target_fps
        
        while self.running:
            if not self.paused:
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time
                
                try:
                    # Update game engine
                    self.game_engine.update(delta_time)
                    
                    # Update GUI components (thread-safe)
                    self.root.after(0, self.update_gui)
                    
                except Exception as e:
                    print(f"Game loop error: {e}")
                    self.running = False
                    
            time.sleep(frame_time)
            
    def update_gui(self):
        """Update GUI components (called from main thread)"""
        if self.game_engine:
            self.world_view.update_display()
            self.status_panel.update_display()
            self.debug_panel.update_display()
            
    def speed_up(self):
        """Increase simulation speed"""
        # Implementation depends on game engine
        pass
        
    def slow_down(self):
        """Decrease simulation speed"""
        # Implementation depends on game engine
        pass
        
    def zoom_in(self):
        """Zoom in the world view"""
        self.world_view.zoom_in()
        
    def zoom_out(self):
        """Zoom out the world view"""
        self.world_view.zoom_out()
        
    def reset_view(self):
        """Reset the world view"""
        self.world_view.reset_view()
        
    def toggle_debug(self):
        """Toggle debug information display"""
        self.debug_panel.toggle_visibility()
        
    def show_controls(self):
        """Show controls help"""
        controls_text = """
🎮 Dwarf Fortress Simulation Controls

🖱️ Mouse Controls:
• Left Click: Select tile/entity
• Right Click: Context menu
• Mouse Wheel: Zoom in/out
• Middle Click + Drag: Pan view

⌨️ Keyboard Shortcuts:
• WASD: Move camera
• Q/E: Change Z-level
• Space: Pause/Resume
• R: Reset view
• F1: Toggle debug info

🎛️ Menu Options:
• File → New World: Generate new world
• File → Load/Save: Manage save files
• Simulation → Start/Pause/Stop: Control simulation
• View → Zoom/Debug: Display options

🏗️ World Generation:
• Adjust world size and parameters
• Set number of initial dwarves
• Choose biome preferences
• Enable debug features
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Controls Help")
        help_window.geometry("500x600")
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, controls_text)
        text_widget.config(state=tk.DISABLED)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
🏰 Dwarf Fortress Simulation v1.0.0

A comprehensive dwarf fortress-style simulation featuring:
• Procedural world generation with 3D Perlin noise
• AI-driven dwarf agents with needs and mood systems
• A* pathfinding with z-level navigation
• Resource management and production chains
• Multi-layer physics simulation
• Performance optimized for 60 FPS

Created with Python and Tkinter
Licensed under MIT License

GitHub: https://github.com/kevshakes/dwarf-fortress-simulation
        """
        messagebox.showinfo("About", about_text)
        
    def update_status(self, message):
        """Update the status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        
    def on_closing(self):
        """Handle window closing"""
        if self.running:
            if messagebox.askokcancel("Quit", "Simulation is running. Do you want to quit?"):
                self.stop_simulation()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
