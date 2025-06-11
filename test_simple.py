#!/usr/bin/env python3
"""
Simple test without external dependencies
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """Test core functionality without external dependencies"""
    try:
        # Test configuration
        from core.config import GameConfig, Constants
        config = GameConfig(world_size=16, z_levels=5, initial_dwarves=2)
        print(f"✓ Config: {config.world_size}x{config.world_size}x{config.z_levels}")
        
        # Test simplified world state
        from world.world_state_simple import WorldState, Tile, Biome
        world_state = WorldState(config.world_size, config.z_levels)
        print(f"✓ World state: {world_state.size}x{world_state.size}x{world_state.z_levels}")
        
        # Test tile operations
        tile = world_state.get_tile(0, 0, 0)
        tile.material = Constants.TILE_STONE
        world_state.set_tile(0, 0, 0, tile)
        retrieved_tile = world_state.get_tile(0, 0, 0)
        print(f"✓ Tile operations: material={retrieved_tile.material}")
        
        # Test biome
        biome = Biome(Constants.BIOME_FOREST, 0.5, 0.7, 0.3)
        world_state.set_biome(5, 5, biome)
        retrieved_biome = world_state.get_biome(5, 5)
        print(f"✓ Biome operations: type={retrieved_biome.type}")
        
        # Test noise generator
        from utils.noise import PerlinNoise3D
        noise = PerlinNoise3D(42)
        sample = noise.sample(1.0, 1.0, 1.0)
        print(f"✓ Noise generator: sample={sample:.3f}")
        
        # Test dwarf (using simplified world state)
        from entities.dwarf import Dwarf
        dwarf = Dwarf(1, (5, 5, 2), world_state)
        print(f"✓ Dwarf: {dwarf.name} at {dwarf.position}")
        
        # Test dwarf needs update
        dwarf.update(1.0)  # 1 second
        print(f"✓ Dwarf update: food={dwarf.needs['food']:.1f}, mood={dwarf.mood:.2f}")
        
        # Test pathfinding setup
        from ai.pathfinding import AStarPathfinder
        pathfinder = AStarPathfinder(world_state, 50)
        print("✓ Pathfinder created")
        
        # Test simple pathfinding
        start = (0, 0, 0)
        goal = (2, 2, 0)
        path = pathfinder.find_path(start, goal)
        if path:
            print(f"✓ Pathfinding: found path with {len(path)} steps")
        else:
            print("✓ Pathfinding: no path found (expected for solid tiles)")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_systems():
    """Test AI systems"""
    try:
        from core.config import GameConfig
        from world.world_state_simple import WorldState
        from entities.dwarf import Dwarf
        from ai.decision_tree import DecisionTree, Decision
        from ai.needs_system import NeedsSystem
        
        config = GameConfig()
        world_state = WorldState(16, 5)
        dwarf = Dwarf(1, (5, 5, 2), world_state)
        
        # Test decision tree
        decision_tree = DecisionTree(config)
        decision = decision_tree.make_decision(dwarf, world_state)
        print(f"✓ Decision tree: action={decision.action_type}")
        
        # Test needs system
        needs_system = NeedsSystem(config)
        urgent_need = needs_system.get_most_urgent_need(dwarf)
        print(f"✓ Needs system: urgent_need={urgent_need}")
        
        return True
        
    except Exception as e:
        print(f"✗ AI systems error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resource_systems():
    """Test resource management systems"""
    try:
        from resources.item import Item, ItemType
        from resources.stockpile import Stockpile
        
        # Test item system
        item_type = ItemType.get_type('iron_ore')
        item = Item(1, item_type, (10, 10, 5), 5)
        print(f"✓ Item system: {item.quantity} {item.item_type.name}")
        
        # Test stockpile
        stockpile = Stockpile((10, 10, 5), (3, 3, 1))
        added = stockpile.add_item('iron_ore', 10)
        count = stockpile.get_item_count('iron_ore')
        print(f"✓ Stockpile: added {added}, count {count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Resource systems error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive tests"""
    print("Dwarf Fortress Simulation - Comprehensive Test")
    print("=" * 50)
    
    tests = [
        ("Core Functionality", test_core_functionality),
        ("AI Systems", test_ai_systems),
        ("Resource Systems", test_resource_systems)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            print(f"✓ {test_name} passed")
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The simulation core is working.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install numpy psutil colorama")
        print("2. Run full simulation: python main.py --ascii --dwarves 3")
        print("3. Try debug mode: python main.py --debug --ascii")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
