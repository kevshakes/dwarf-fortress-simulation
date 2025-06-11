#!/usr/bin/env python3
"""
Quick run script for the Dwarf Fortress Simulation
"""

import subprocess
import sys
import os

def main():
    """Run the simulation with common configurations"""
    print("Dwarf Fortress Simulation Launcher")
    print("=" * 40)
    print("1. Normal simulation (10 dwarves)")
    print("2. Debug mode with pathfinding visualization")
    print("3. Stress test (100 entities)")
    print("4. Performance benchmark")
    print("5. Custom parameters")
    print("6. ASCII mode only")
    
    choice = input("\nSelect option (1-6): ").strip()
    
    base_cmd = [sys.executable, "main.py"]
    
    if choice == "1":
        cmd = base_cmd + ["--dwarves", "10"]
    elif choice == "2":
        cmd = base_cmd + ["--debug", "--debug-pathfinding", "--dwarves", "5"]
    elif choice == "3":
        cmd = base_cmd + ["--generate", "stress_test"]
    elif choice == "4":
        cmd = base_cmd + ["--generate", "benchmark"]
    elif choice == "5":
        print("\nCustom parameters:")
        world_size = input("World size (default 128): ").strip() or "128"
        z_levels = input("Z levels (default 20): ").strip() or "20"
        dwarves = input("Number of dwarves (default 10): ").strip() or "10"
        debug = input("Debug mode? (y/n): ").strip().lower() == 'y'
        
        cmd = base_cmd + [
            "--world-size", world_size,
            "--z-levels", z_levels,
            "--dwarves", dwarves
        ]
        if debug:
            cmd.append("--debug")
    elif choice == "6":
        cmd = base_cmd + ["--ascii", "--dwarves", "10"]
    else:
        print("Invalid choice, using default settings")
        cmd = base_cmd + ["--dwarves", "10"]
    
    print(f"\nRunning: {' '.join(cmd)}")
    print("Press Ctrl+C to stop the simulation")
    print("-" * 40)
    
    try:
        subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    except Exception as e:
        print(f"Error running simulation: {e}")

if __name__ == "__main__":
    main()
