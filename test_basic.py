#!/usr/bin/env python3
"""
Basic test of the simulation without external dependencies
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from core.config import GameConfig, Constants
        print("✓ Core config imported")
        
        from world.world_state import WorldState, Tile
        print("✓ World state imported")
        
        from entities.dwarf import Dwarf
        print("✓ Dwarf entity imported")
        
        from ai.pathfinding import AStarPathfinder
        print("✓ Pathfinding imported")
        
        from utils.noise import PerlinNoise3D
        print("✓ Noise generator imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    try:
        # Test configuration
        config = GameConfig(world_size=32, z_levels=10, initial_dwarves=3)
        print(f"✓ Config created: {config.world_size}x{config.world_size}x{config.z_levels}")
        
        # Test world state
        world_state = WorldState(config.world_size, config.z_levels)
        print(f"✓ World state created: {world_state.size}x{world_state.size}x{world_state.z_levels}")
        
        # Test tile access
        tile = world_state.get_tile(0, 0, 0)
        print(f"✓ Tile access works: material={tile.material}")
        
        # Test noise generator
        noise = PerlinNoise3D(42)
        sample = noise.sample(1.0, 1.0, 1.0)
        print(f"✓ Noise generator works: sample={sample:.3f}")
        
        # Test dwarf creation
        dwarf = Dwarf(1, (5, 5, 5), world_state)
        print(f"✓ Dwarf created: {dwarf.name} at {dwarf.position}")
        
        # Test pathfinding setup
        pathfinder = AStarPathfinder(world_state, 100)
        print("✓ Pathfinder created")
        
        return True
    except Exception as e:
        print(f"✗ Functionality error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic tests"""
    print("Dwarf Fortress Simulation - Basic Test")
    print("=" * 40)
    
    if not test_imports():
        print("Import tests failed!")
        return False
        
    print("\nTesting basic functionality...")
    if not test_basic_functionality():
        print("Functionality tests failed!")
        return False
        
    print("\n✓ All basic tests passed!")
    print("The simulation core is working correctly.")
    print("\nTo run the full simulation:")
    print("1. Install required packages: numpy, psutil, colorama")
    print("2. Run: python main.py --ascii --dwarves 5")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
