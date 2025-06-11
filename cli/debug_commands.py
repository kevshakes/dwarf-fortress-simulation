"""
CLI debug commands for the simulation
"""

import re
from typing import Dict, Any, List
from core.game_engine import GameEngine

class DebugCommandHandler:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.commands = {
            'debug': self.handle_debug_command,
            'optimize': self.handle_optimize_command,
            'generate': self.handle_generate_command,
            'stats': self.handle_stats_command,
            'save': self.handle_save_command,
            'load': self.handle_load_command,
            'spawn': self.handle_spawn_command,
            'teleport': self.handle_teleport_command,
            'resources': self.handle_resources_command,
            'pathfind': self.handle_pathfind_command
        }
        
    def execute_command(self, command_line: str) -> str:
        """Execute a debug command and return result"""
        parts = command_line.strip().split()
        if not parts:
            return "No command specified"
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if command in self.commands:
            try:
                return self.commands[command](args)
            except Exception as e:
                return f"Error executing command '{command}': {e}"
        else:
            return f"Unknown command: {command}. Available commands: {', '.join(self.commands.keys())}"
            
    def handle_debug_command(self, args: List[str]) -> str:
        """Handle debug visualization commands"""
        if not args:
            return "Debug options: pathfinding, ai_decisions, resource_flows, performance"
            
        debug_type = args[0].lower()
        
        if debug_type == "pathfinding":
            action = args[1] if len(args) > 1 else "toggle"
            if action == "on" or action == "toggle":
                self.engine.config.show_pathfinding = True
                return "Pathfinding debug visualization enabled"
            elif action == "off":
                self.engine.config.show_pathfinding = False
                return "Pathfinding debug visualization disabled"
                
        elif debug_type == "ai_decisions":
            action = args[1] if len(args) > 1 else "toggle"
            if action == "on" or action == "toggle":
                self.engine.config.show_ai_decisions = True
                return "AI decisions debug visualization enabled"
            elif action == "off":
                self.engine.config.show_ai_decisions = False
                return "AI decisions debug visualization disabled"
                
        elif debug_type == "resource_flows":
            action = args[1] if len(args) > 1 else "toggle"
            if action == "on" or action == "toggle":
                self.engine.config.show_resource_flows = True
                return "Resource flows debug visualization enabled"
            elif action == "off":
                self.engine.config.show_resource_flows = False
                return "Resource flows debug visualization disabled"
                
        elif debug_type == "performance":
            action = args[1] if len(args) > 1 else "toggle"
            if action == "on" or action == "toggle":
                self.engine.config.show_performance_stats = True
                return "Performance stats enabled"
            elif action == "off":
                self.engine.config.show_performance_stats = False
                return "Performance stats disabled"
                
        return f"Unknown debug type: {debug_type}"
        
    def handle_optimize_command(self, args: List[str]) -> str:
        """Handle optimization commands"""
        if not args:
            return "Optimize options: spatial_partitioning, pathfinding_cache, memory"
            
        optimize_type = args[0].lower()
        
        if optimize_type == "spatial_partitioning":
            # Parse grid_size parameter
            grid_size = 64  # default
            for arg in args[1:]:
                if arg.startswith("grid_size="):
                    try:
                        grid_size = int(arg.split("=")[1])
                    except ValueError:
                        return "Invalid grid_size value"
                        
            self.engine.config.spatial_grid_size = grid_size
            self.engine.spatial_partition.resize_grid(grid_size)
            return f"Spatial partitioning grid size set to {grid_size}"
            
        elif optimize_type == "pathfinding_cache":
            action = args[1] if len(args) > 1 else "clear"
            if action == "clear":
                self.engine.ai_manager.pathfinder.clear_cache()
                return "Pathfinding cache cleared"
            elif action == "stats":
                cache_size = self.engine.ai_manager.pathfinder.get_cache_size()
                return f"Pathfinding cache size: {cache_size} entries"
                
        elif optimize_type == "memory":
            import gc
            gc.collect()
            memory_usage = self.engine.get_memory_usage()
            return f"Garbage collection performed. Memory usage: {memory_usage:.1f} MB"
            
        return f"Unknown optimization type: {optimize_type}"
        
    def handle_generate_command(self, args: List[str]) -> str:
        """Handle test scenario generation"""
        if not args:
            return "Generate options: test_scenario, stress_test, benchmark"
            
        scenario_type = args[0].lower()
        
        if scenario_type == "test_scenario":
            # Parse dwarf count
            dwarf_count = 10  # default
            if len(args) > 1:
                match = re.search(r'(\d+)_dwarves', args[1])
                if match:
                    dwarf_count = int(match.group(1))
                    
            # Create additional dwarves
            current_count = len(self.engine.entity_manager.get_entities_by_type('dwarf'))
            additional_dwarves = max(0, dwarf_count - current_count)
            
            if additional_dwarves > 0:
                self.engine.entity_manager.create_initial_dwarves(additional_dwarves)
                return f"Created {additional_dwarves} additional dwarves (total: {dwarf_count})"
            else:
                return f"Already have {current_count} dwarves (requested: {dwarf_count})"
                
        elif scenario_type == "stress_test":
            # Create maximum entities for stress testing
            max_entities = self.engine.config.max_agents
            current_count = self.engine.entity_manager.get_entity_count()
            additional = max_entities - current_count
            
            if additional > 0:
                self.engine.entity_manager.create_initial_dwarves(additional)
                return f"Stress test: created {additional} entities (total: {max_entities})"
            else:
                return f"Already at maximum entity count: {current_count}"
                
        elif scenario_type == "benchmark":
            # Run performance benchmark
            import time
            start_time = time.time()
            
            # Run simulation for a few frames
            for _ in range(60):  # 1 second at 60 FPS
                self.engine.update(1.0/60.0)
                
            elapsed = time.time() - start_time
            avg_frame_time = elapsed / 60.0
            estimated_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            
            return f"Benchmark: {elapsed:.2f}s for 60 frames, avg {avg_frame_time*1000:.1f}ms/frame, est. {estimated_fps:.1f} FPS"
            
        return f"Unknown scenario type: {scenario_type}"
        
    def handle_stats_command(self, args: List[str]) -> str:
        """Handle statistics display"""
        stats = []
        stats.append(f"FPS: {self.engine.current_fps}")
        stats.append(f"Entities: {self.engine.entity_manager.get_entity_count()}")
        stats.append(f"Memory: {self.engine.get_memory_usage():.1f} MB")
        stats.append(f"Pathfinding cache: {self.engine.ai_manager.get_pathfinding_cache_size()}")
        
        # Entity breakdown
        dwarves = len(self.engine.entity_manager.get_entities_by_type('dwarf'))
        stats.append(f"Dwarves: {dwarves}")
        
        # Resource stats
        if hasattr(self.engine, 'resource_manager'):
            stockpiles = len(self.engine.resource_manager.stockpile_manager.get_all_stockpiles())
            stats.append(f"Stockpiles: {stockpiles}")
            
        return "\n".join(stats)
        
    def handle_save_command(self, args: List[str]) -> str:
        """Handle save game command"""
        filename = args[0] if args else "debug_save.dat"
        self.engine.save_game(filename)
        return f"Game saved to {filename}"
        
    def handle_load_command(self, args: List[str]) -> str:
        """Handle load game command"""
        filename = args[0] if args else "debug_save.dat"
        try:
            self.engine.load_game(filename)
            return f"Game loaded from {filename}"
        except FileNotFoundError:
            return f"Save file not found: {filename}"
        except Exception as e:
            return f"Error loading game: {e}"
            
    def handle_spawn_command(self, args: List[str]) -> str:
        """Handle entity spawning"""
        if len(args) < 4:
            return "Usage: spawn <type> <x> <y> <z>"
            
        entity_type = args[0].lower()
        try:
            x, y, z = int(args[1]), int(args[2]), int(args[3])
        except ValueError:
            return "Invalid coordinates"
            
        if entity_type == "dwarf":
            dwarf = self.engine.entity_manager.create_dwarf(x, y, z)
            return f"Spawned dwarf '{dwarf.name}' at ({x}, {y}, {z})"
        else:
            return f"Unknown entity type: {entity_type}"
            
    def handle_teleport_command(self, args: List[str]) -> str:
        """Handle entity teleportation"""
        if len(args) < 4:
            return "Usage: teleport <entity_id> <x> <y> <z>"
            
        try:
            entity_id = int(args[0])
            x, y, z = int(args[1]), int(args[2]), int(args[3])
        except ValueError:
            return "Invalid parameters"
            
        entity = self.engine.entity_manager.get_entity(entity_id)
        if entity:
            entity.position = (x, y, z)
            return f"Teleported entity {entity_id} to ({x}, {y}, {z})"
        else:
            return f"Entity {entity_id} not found"
            
    def handle_resources_command(self, args: List[str]) -> str:
        """Handle resource management commands"""
        if not args:
            return "Resource options: list, add, remove, flow"
            
        action = args[0].lower()
        
        if action == "list":
            # List global resources
            resources = []
            for stockpile in self.engine.resource_manager.stockpile_manager.get_all_stockpiles():
                for item_type, count in stockpile.items.items():
                    resources.append(f"{item_type}: {count}")
            return "\n".join(resources) if resources else "No resources found"
            
        elif action == "add":
            if len(args) < 3:
                return "Usage: resources add <type> <quantity>"
            item_type = args[1]
            try:
                quantity = int(args[2])
            except ValueError:
                return "Invalid quantity"
                
            # Add to first available stockpile
            stockpiles = self.engine.resource_manager.stockpile_manager.get_all_stockpiles()
            if stockpiles:
                stockpiles[0].add_item(item_type, quantity)
                return f"Added {quantity} {item_type} to stockpile"
            else:
                return "No stockpiles available"
                
        return f"Unknown resource action: {action}"
        
    def handle_pathfind_command(self, args: List[str]) -> str:
        """Handle pathfinding testing"""
        if len(args) < 6:
            return "Usage: pathfind <start_x> <start_y> <start_z> <end_x> <end_y> <end_z>"
            
        try:
            start = (int(args[0]), int(args[1]), int(args[2]))
            end = (int(args[3]), int(args[4]), int(args[5]))
        except ValueError:
            return "Invalid coordinates"
            
        path = self.engine.ai_manager.find_path(start, end)
        if path:
            return f"Path found: {len(path)} steps from {start} to {end}"
        else:
            return f"No path found from {start} to {end}"
            
    def enable_pathfinding_debug(self):
        """Enable pathfinding debug visualization"""
        self.engine.config.show_pathfinding = True
        
    def handle_optimize_command(self, command: str) -> str:
        """Handle optimization commands from CLI args"""
        if "spatial_partitioning" in command:
            # Extract grid_size parameter
            match = re.search(r'grid_size=(\d+)', command)
            if match:
                grid_size = int(match.group(1))
                self.engine.config.spatial_grid_size = grid_size
                return f"Spatial partitioning optimized with grid size {grid_size}"
        return "Optimization applied"
        
    def handle_generate_command(self, command: str) -> str:
        """Handle generate commands from CLI args"""
        if "test_scenario" in command:
            # Extract dwarf count
            match = re.search(r'(\d+)_dwarves', command)
            if match:
                dwarf_count = int(match.group(1))
                current_count = len(self.engine.entity_manager.get_entities_by_type('dwarf'))
                additional = max(0, dwarf_count - current_count)
                if additional > 0:
                    self.engine.entity_manager.create_initial_dwarves(additional)
                return f"Generated test scenario with {dwarf_count} dwarves"
        return "Test scenario generated"
