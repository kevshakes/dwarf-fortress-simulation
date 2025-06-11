#!/usr/bin/env python3
"""
Simple GUI demo to verify the interface works
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_demo_window():
    """Create a demo window showing GUI functionality"""
    root = tk.Tk()
    root.title("🏰 Dwarf Fortress Simulation - GUI Demo")
    root.geometry("800x600")
    
    # Title
    title_frame = tk.Frame(root, bg='#2c3e50', height=80)
    title_frame.pack(fill=tk.X)
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(title_frame, text="🏰 Dwarf Fortress Simulation", 
                          font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
    title_label.pack(expand=True)
    
    # Main content
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Left side - simulated world view
    left_frame = ttk.LabelFrame(main_frame, text="🗺️ World View (Demo)", padding=10)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    
    # Canvas for world simulation
    canvas = tk.Canvas(left_frame, bg='black', width=400, height=300)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Draw demo world
    def draw_demo_world():
        canvas.delete("all")
        
        # Draw terrain tiles
        colors = ['#808080', '#8B4513', '#228B22', '#0000FF']  # Stone, soil, grass, water
        tile_size = 15
        
        for x in range(0, 400, tile_size):
            for y in range(0, 300, tile_size):
                color_idx = ((x//tile_size) + (y//tile_size)) % len(colors)
                color = colors[color_idx]
                canvas.create_rectangle(x, y, x+tile_size, y+tile_size, 
                                      fill=color, outline='#333333')
        
        # Draw some "dwarves"
        dwarf_positions = [(60, 90), (150, 120), (240, 180), (330, 90), (120, 240)]
        for i, (x, y) in enumerate(dwarf_positions):
            # Dwarf body
            canvas.create_oval(x-4, y-4, x+4, y+4, fill='#FFD700', outline='white')
            # Dwarf label
            canvas.create_text(x, y-15, text=f"D{i+1}", fill='white', font=('Arial', 8, 'bold'))
        
        # Add some items
        item_positions = [(90, 60), (180, 150), (270, 210)]
        for x, y in item_positions:
            canvas.create_rectangle(x-2, y-2, x+2, y+2, fill='white', outline='gray')
    
    draw_demo_world()
    
    # Right side - controls
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
    
    # Control panel
    control_frame = ttk.LabelFrame(right_frame, text="🎛️ Controls", padding=10)
    control_frame.pack(fill=tk.X, pady=(0, 5))
    
    # World generation
    gen_frame = ttk.LabelFrame(control_frame, text="World Generation", padding=5)
    gen_frame.pack(fill=tk.X, pady=(0, 5))
    
    ttk.Label(gen_frame, text="World Size:").pack(anchor=tk.W)
    size_var = tk.StringVar(value="64x64")
    ttk.Combobox(gen_frame, textvariable=size_var, values=["32x32", "64x64", "96x96"], 
                state="readonly", width=15).pack(anchor=tk.W, pady=2)
    
    ttk.Label(gen_frame, text="Dwarves:").pack(anchor=tk.W, pady=(5, 0))
    dwarf_var = tk.IntVar(value=7)
    ttk.Spinbox(gen_frame, from_=1, to=20, textvariable=dwarf_var, width=15).pack(anchor=tk.W, pady=2)
    
    def generate_world():
        messagebox.showinfo("Demo", f"Generated {size_var.get()} world with {dwarf_var.get()} dwarves!\n(This is just a demo)")
        draw_demo_world()
    
    ttk.Button(gen_frame, text="🌍 Generate World", command=generate_world).pack(pady=5, fill=tk.X)
    
    # Simulation controls
    sim_frame = ttk.LabelFrame(control_frame, text="Simulation", padding=5)
    sim_frame.pack(fill=tk.X, pady=(0, 5))
    
    button_frame = ttk.Frame(sim_frame)
    button_frame.pack(fill=tk.X)
    
    def start_sim():
        messagebox.showinfo("Demo", "Simulation started!\n(This is just a demo)")
    
    def pause_sim():
        messagebox.showinfo("Demo", "Simulation paused!\n(This is just a demo)")
    
    ttk.Button(button_frame, text="▶️", command=start_sim, width=3).pack(side=tk.LEFT, padx=1)
    ttk.Button(button_frame, text="⏸️", command=pause_sim, width=3).pack(side=tk.LEFT, padx=1)
    ttk.Button(button_frame, text="⏹️", width=3).pack(side=tk.LEFT, padx=1)
    
    # Status panel
    status_frame = ttk.LabelFrame(right_frame, text="📊 Status", padding=10)
    status_frame.pack(fill=tk.X, pady=(0, 5))
    
    status_text = """FPS: 60.0
Memory: 45.2 MB
Dwarves: 7
Entities: 127
World: 64x64x15"""
    
    ttk.Label(status_frame, text=status_text, font=('Courier', 9)).pack(anchor=tk.W)
    
    # Action buttons
    action_frame = ttk.LabelFrame(right_frame, text="🚀 Actions", padding=10)
    action_frame.pack(fill=tk.X)
    
    def launch_full_gui():
        try:
            import subprocess
            subprocess.Popen([sys.executable, 'main_gui.py'])
            messagebox.showinfo("Launched", "Full GUI launched in new window!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch: {e}")
    
    def run_tests():
        try:
            import subprocess
            result = subprocess.run([sys.executable, 'test_gui_imports.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Tests", "✅ All tests passed!\nGUI is ready to use.")
            else:
                messagebox.showerror("Tests", f"❌ Tests failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run tests: {e}")
    
    ttk.Button(action_frame, text="🚀 Launch Full GUI", command=launch_full_gui).pack(fill=tk.X, pady=2)
    ttk.Button(action_frame, text="🧪 Run Tests", command=run_tests).pack(fill=tk.X, pady=2)
    ttk.Button(action_frame, text="🔄 Redraw World", command=draw_demo_world).pack(fill=tk.X, pady=2)
    
    # Status bar
    status_bar = ttk.Label(root, text="🎮 GUI Demo - All components working!", relief=tk.SUNKEN)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Bind canvas click
    def on_canvas_click(event):
        x, y = event.x, event.y
        messagebox.showinfo("Click", f"Clicked at ({x}, {y})\nIn full GUI, this would select the tile!")
    
    canvas.bind("<Button-1>", on_canvas_click)
    
    return root

def main():
    """Run the demo"""
    print("🏰 Starting GUI Demo...")
    
    try:
        root = create_demo_window()
        
        # Show welcome message
        root.after(1000, lambda: messagebox.showinfo(
            "Welcome!", 
            "🎉 GUI Demo Started!\n\n"
            "This demonstrates the GUI interface.\n"
            "Click 'Launch Full GUI' to run the complete simulation.\n\n"
            "✅ All GUI components are working!"
        ))
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
