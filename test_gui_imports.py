#!/usr/bin/env python3
"""
Test GUI imports to identify any issues
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all GUI imports"""
    print("🧪 Testing GUI Imports")
    print("=" * 25)
    
    # Test 1: Basic tkinter
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        print("✅ tkinter imports successful")
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False
    
    # Test 2: Core components
    try:
        from core.config import GameConfig, Constants
        print("✅ Core config imports successful")
    except ImportError as e:
        print(f"❌ Core config import failed: {e}")
        return False
    
    # Test 3: Game engine
    try:
        from core.game_engine_gui import GameEngineGUI
        print("✅ Game engine import successful")
    except ImportError as e:
        print(f"❌ Game engine import failed: {e}")
        print(f"   Error details: {e}")
        return False
    
    # Test 4: GUI components
    try:
        from gui.world_view import WorldView
        print("✅ WorldView import successful")
    except ImportError as e:
        print(f"❌ WorldView import failed: {e}")
        return False
    
    try:
        from gui.control_panel import ControlPanel
        print("✅ ControlPanel import successful")
    except ImportError as e:
        print(f"❌ ControlPanel import failed: {e}")
        return False
    
    try:
        from gui.status_panel import StatusPanel, DebugPanel
        print("✅ StatusPanel and DebugPanel imports successful")
    except ImportError as e:
        print(f"❌ StatusPanel/DebugPanel import failed: {e}")
        return False
    
    # Test 5: Main window
    try:
        from gui.main_window import MainWindow
        print("✅ MainWindow import successful")
    except ImportError as e:
        print(f"❌ MainWindow import failed: {e}")
        print(f"   Error details: {e}")
        return False
    
    print("\n🎉 All imports successful!")
    return True

def test_basic_functionality():
    """Test basic GUI functionality"""
    print("\n🔧 Testing Basic Functionality")
    print("=" * 30)
    
    try:
        # Test config creation
        from core.config import GameConfig
        config = GameConfig(world_size=32, z_levels=10, initial_dwarves=3)
        print("✅ Config creation successful")
        
        # Test game engine creation
        from core.game_engine_gui import GameEngineGUI
        engine = GameEngineGUI(config)
        print("✅ Game engine creation successful")
        
        # Test basic GUI window creation
        import tkinter as tk
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("200x100")
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ Basic GUI window creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🏰 GUI Import and Functionality Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 All tests passed!")
            print("🚀 GUI should work correctly now.")
            print("\nTry running:")
            print("  python3 main_gui.py")
            print("  python3 launch.py")
            return True
        else:
            print("\n❌ Functionality tests failed.")
            return False
    else:
        print("\n❌ Import tests failed.")
        print("Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
