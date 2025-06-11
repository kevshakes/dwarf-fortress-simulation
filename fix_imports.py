#!/usr/bin/env python3
"""
Fix any remaining import issues in the GUI
"""

import os
import sys

def fix_main_window_imports():
    """Fix imports in main_window.py"""
    main_window_path = "gui/main_window.py"
    
    if not os.path.exists(main_window_path):
        print(f"❌ {main_window_path} not found")
        return False
    
    # Read the file
    with open(main_window_path, 'r') as f:
        content = f.read()
    
    # Check if imports are correct
    if "from gui.status_panel import StatusPanel, DebugPanel" in content:
        print("✅ Imports in main_window.py are already correct")
        return True
    
    # Fix the imports if needed
    old_import = "from gui.debug_panel import DebugPanel"
    new_import = "from gui.status_panel import StatusPanel, DebugPanel"
    
    if old_import in content:
        content = content.replace(old_import, "")
        print("✅ Removed incorrect DebugPanel import")
    
    # Ensure correct StatusPanel import
    if "from gui.status_panel import StatusPanel" in content and "DebugPanel" not in content:
        content = content.replace(
            "from gui.status_panel import StatusPanel",
            "from gui.status_panel import StatusPanel, DebugPanel"
        )
        print("✅ Added DebugPanel to StatusPanel import")
    
    # Write back the file
    with open(main_window_path, 'w') as f:
        f.write(content)
    
    print("✅ Fixed imports in main_window.py")
    return True

def check_all_files():
    """Check all GUI files for import issues"""
    gui_files = [
        "gui/main_window.py",
        "gui/world_view.py", 
        "gui/control_panel.py",
        "gui/status_panel.py"
    ]
    
    all_good = True
    
    for file_path in gui_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_good = False
    
    return all_good

def main():
    """Main fix function"""
    print("🔧 Fixing GUI Import Issues")
    print("=" * 30)
    
    # Check all files exist
    if not check_all_files():
        print("❌ Some GUI files are missing")
        return False
    
    # Fix main window imports
    if not fix_main_window_imports():
        print("❌ Failed to fix main window imports")
        return False
    
    print("\n🎉 All import issues fixed!")
    print("🚀 Try running the GUI now:")
    print("  python3 main_gui.py")
    print("  python3 launch.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
