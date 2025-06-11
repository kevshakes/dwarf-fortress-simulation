#!/usr/bin/env python3
"""
Main GUI launcher for Dwarf Fortress Simulation
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check for required dependencies and show status"""
    missing_deps = []
    optional_deps = []
    
    # Check tkinter (should be included with Python)
    try:
        import tkinter
        import tkinter.ttk
    except ImportError:
        missing_deps.append("tkinter (GUI framework)")
    
    # Check optional dependencies
    try:
        import psutil
    except ImportError:
        optional_deps.append("psutil (performance monitoring)")
        
    try:
        import numpy
    except ImportError:
        optional_deps.append("numpy (enhanced world generation)")
        
    try:
        import colorama
    except ImportError:
        optional_deps.append("colorama (terminal colors)")
    
    return missing_deps, optional_deps

def show_dependency_info():
    """Show dependency information dialog"""
    missing, optional = check_dependencies()
    
    if missing:
        message = "❌ Missing required dependencies:\n"
        for dep in missing:
            message += f"  • {dep}\n"
        message += "\nPlease install missing dependencies and try again."
        messagebox.showerror("Missing Dependencies", message)
        return False
    
    if optional:
        message = "⚠️ Optional dependencies not found:\n"
        for dep in optional:
            message += f"  • {dep}\n"
        message += "\nThe simulation will work with reduced functionality.\n"
        message += "Install with: pip install -r requirements_gui.txt"
        
        result = messagebox.askquestion(
            "Optional Dependencies", 
            message + "\n\nContinue anyway?",
            icon='warning'
        )
        return result == 'yes'
    
    return True

def main():
    """Main entry point"""
    print("🏰 Dwarf Fortress Simulation - GUI Version")
    print("=" * 50)
    
    # Check dependencies
    if not show_dependency_info():
        print("Dependency check failed. Exiting.")
        return
    
    try:
        # Import GUI components
        from gui.main_window import MainWindow
        
        print("Starting GUI application...")
        
        # Create and run the main window
        app = MainWindow()
        app.run()
        
    except ImportError as e:
        error_msg = f"Failed to import GUI components: {e}\n\n"
        error_msg += "This might be due to missing dependencies or incorrect installation.\n"
        error_msg += "Please check that all files are present and try again."
        
        print(f"Error: {error_msg}")
        
        # Try to show error in GUI if tkinter is available
        try:
            root = tk.Tk()
            root.withdraw()  # Hide main window
            messagebox.showerror("Import Error", error_msg)
        except:
            pass  # If even tkinter fails, just print to console
            
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"Error: {error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
        except:
            pass

if __name__ == "__main__":
    main()
