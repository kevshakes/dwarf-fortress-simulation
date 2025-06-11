#!/usr/bin/env python3
"""
Dwarf Fortress-style Simulation Game
Main entry point and game loop
"""

import sys
import time
import argparse
from typing import Dict, Any
from core.game_engine import GameEngine
from core.config import GameConfig
from cli.debug_commands import DebugCommandHandler
from utils.performance import PerformanceMonitor

class DwarfFortressSimulation:
    def __init__(self, config: GameConfig):
        self.config = config
        self.engine = GameEngine(config)
        self.debug_handler = DebugCommandHandler(self.engine)
        self.performance_monitor = PerformanceMonitor()
        self.running = False
        
    def initialize(self):
        """Initialize all game systems"""
        print("Initializing Dwarf Fortress Simulation...")
        self.engine.initialize()
        print("Game systems initialized successfully!")
        
    def run(self):
        """Main game loop"""
        self.running = True
        last_time = time.time()
        target_fps = 60
        frame_time = 1.0 / target_fps
        
        print(f"Starting simulation at {target_fps} FPS...")
        
        while self.running:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Update game systems
            self.performance_monitor.start_frame()
            
            try:
                self.engine.update(delta_time)
                self.engine.render()
                
                # Handle CLI commands if any
                self.handle_cli_input()
                
            except KeyboardInterrupt:
                print("\nShutting down simulation...")
                self.running = False
                break
            except Exception as e:
                print(f"Error in game loop: {e}")
                if self.config.debug_mode:
                    import traceback
                    traceback.print_exc()
                    
            self.performance_monitor.end_frame()
            
            # Frame rate limiting
            elapsed = time.time() - current_time
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)
                
        self.shutdown()
        
    def handle_cli_input(self):
        """Handle CLI debug commands"""
        # Non-blocking input handling would go here
        # For now, we'll handle commands through command line args
        pass
        
    def shutdown(self):
        """Clean shutdown"""
        print("Saving game state...")
        self.engine.save_game("autosave.dat")
        print("Simulation ended.")

def main():
    parser = argparse.ArgumentParser(description='Dwarf Fortress Simulation')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--ascii', action='store_true', help='Use ASCII rendering')
    parser.add_argument('--world-size', type=int, default=128, help='World size')
    parser.add_argument('--z-levels', type=int, default=20, help='Number of Z levels')
    parser.add_argument('--dwarves', type=int, default=10, help='Initial dwarf count')
    
    # Debug commands
    parser.add_argument('--debug-pathfinding', action='store_true', help='Show pathfinding debug')
    parser.add_argument('--optimize', type=str, help='Optimization command')
    parser.add_argument('--generate', type=str, help='Generate test scenario')
    
    args = parser.parse_args()
    
    # Create configuration
    config = GameConfig(
        debug_mode=args.debug,
        ascii_mode=args.ascii,
        world_size=args.world_size,
        z_levels=args.z_levels,
        initial_dwarves=args.dwarves
    )
    
    # Create and run simulation
    simulation = DwarfFortressSimulation(config)
    
    # Handle CLI commands
    if args.debug_pathfinding:
        simulation.debug_handler.enable_pathfinding_debug()
    if args.optimize:
        simulation.debug_handler.handle_optimize_command(args.optimize)
    if args.generate:
        simulation.debug_handler.handle_generate_command(args.generate)
    
    simulation.initialize()
    simulation.run()

if __name__ == "__main__":
    main()
