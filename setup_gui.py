#!/usr/bin/env python3
"""
Setup and verification script for Dwarf Fortress Simulation GUI
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        return False, f"Python {version.major}.{version.minor}.{version.micro}"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        import tkinter.ttk
        return True, "Available"
    except ImportError as e:
        return False, f"Missing: {e}"

def check_optional_dependencies():
    """Check optional dependencies"""
    deps = {}
    
    # psutil
    try:
        import psutil
        deps['psutil'] = f"✅ {psutil.__version__}"
    except ImportError:
        deps['psutil'] = "❌ Not installed"
    
    # numpy
    try:
        import numpy
        deps['numpy'] = f"✅ {numpy.__version__}"
    except ImportError:
        deps['numpy'] = "❌ Not installed"
    
    # colorama
    try:
        import colorama
        deps['colorama'] = f"✅ {colorama.__version__}"
    except ImportError:
        deps['colorama'] = "❌ Not installed"
    
    return deps

def check_project_structure():
    """Check if all required files are present"""
    required_files = [
        'main_gui.py',
        'test_gui.py',
        'core/config.py',
        'core/game_engine_gui.py',
        'gui/main_window.py',
        'gui/world_view.py',
        'gui/control_panel.py',
        'gui/status_panel.py',
        'world/world_state_simple.py',
        'entities/dwarf_simple.py',
        'ai/pathfinding_simple.py',
        'utils/noise.py',
        'requirements_gui.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    return missing_files

def install_optional_dependencies():
    """Install optional dependencies"""
    try:
        print("Installing optional dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_gui.txt'])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("pip not found. Please install pip first.")
        return False

def run_gui_test():
    """Run the GUI test"""
    try:
        print("Running GUI test...")
        result = subprocess.run([sys.executable, 'test_gui.py'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "GUI test timed out"
    except Exception as e:
        return False, "", str(e)

class SetupGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏰 Dwarf Fortress Simulation - Setup")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.run_checks()
        
    def setup_ui(self):
        """Setup the UI"""
        # Title
        title_label = tk.Label(self.root, text="🏰 Dwarf Fortress Simulation Setup", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # System Check tab
        self.system_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.system_frame, text="System Check")
        
        # Dependencies tab
        self.deps_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.deps_frame, text="Dependencies")
        
        # Installation tab
        self.install_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.install_frame, text="Installation")
        
        # Test tab
        self.test_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.test_frame, text="Test")
        
        self.setup_system_tab()
        self.setup_deps_tab()
        self.setup_install_tab()
        self.setup_test_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to check system...")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_system_tab(self):
        """Setup system check tab"""
        ttk.Label(self.system_frame, text="System Requirements Check", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.system_text = tk.Text(self.system_frame, height=20, width=70, font=('Courier', 10))
        scrollbar1 = ttk.Scrollbar(self.system_frame, orient=tk.VERTICAL, command=self.system_text.yview)
        self.system_text.configure(yscrollcommand=scrollbar1.set)
        
        self.system_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_deps_tab(self):
        """Setup dependencies tab"""
        ttk.Label(self.deps_frame, text="Optional Dependencies", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.deps_text = tk.Text(self.deps_frame, height=20, width=70, font=('Courier', 10))
        scrollbar2 = ttk.Scrollbar(self.deps_frame, orient=tk.VERTICAL, command=self.deps_text.yview)
        self.deps_text.configure(yscrollcommand=scrollbar2.set)
        
        self.deps_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_install_tab(self):
        """Setup installation tab"""
        ttk.Label(self.install_frame, text="Install Optional Dependencies", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        info_text = """
Optional dependencies enhance the simulation but are not required:

• psutil: Performance monitoring and memory usage tracking
• numpy: Enhanced world generation algorithms  
• colorama: Colored terminal output for debugging

The simulation works perfectly without these packages,
but installing them provides the full experience.
        """
        
        ttk.Label(self.install_frame, text=info_text, justify=tk.LEFT).pack(pady=10)
        
        self.install_button = ttk.Button(self.install_frame, text="📦 Install Optional Dependencies", 
                                        command=self.install_dependencies)
        self.install_button.pack(pady=10)
        
        self.install_result = tk.Text(self.install_frame, height=10, width=70, font=('Courier', 9))
        scrollbar3 = ttk.Scrollbar(self.install_frame, orient=tk.VERTICAL, command=self.install_result.yview)
        self.install_result.configure(yscrollcommand=scrollbar3.set)
        
        self.install_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_test_tab(self):
        """Setup test tab"""
        ttk.Label(self.test_frame, text="GUI Test", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(self.test_frame, text="Test the GUI components to ensure everything works correctly.").pack(pady=10)
        
        button_frame = ttk.Frame(self.test_frame)
        button_frame.pack(pady=10)
        
        self.test_button = ttk.Button(button_frame, text="🧪 Run GUI Test", 
                                     command=self.run_test)
        self.test_button.pack(side=tk.LEFT, padx=5)
        
        self.launch_button = ttk.Button(button_frame, text="🚀 Launch Simulation", 
                                       command=self.launch_simulation)
        self.launch_button.pack(side=tk.LEFT, padx=5)
        
        self.test_result = tk.Text(self.test_frame, height=15, width=70, font=('Courier', 9))
        scrollbar4 = ttk.Scrollbar(self.test_frame, orient=tk.VERTICAL, command=self.test_result.yview)
        self.test_result.configure(yscrollcommand=scrollbar4.set)
        
        self.test_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar4.pack(side=tk.RIGHT, fill=tk.Y)
        
    def run_checks(self):
        """Run all system checks"""
        self.status_var.set("Running system checks...")
        self.root.update()
        
        # System checks
        system_report = "🏰 DWARF FORTRESS SIMULATION - SYSTEM CHECK\n"
        system_report += "=" * 50 + "\n\n"
        
        # Python version
        python_ok, python_info = check_python_version()
        system_report += f"Python Version: {python_info}\n"
        system_report += f"Status: {'✅ OK' if python_ok else '❌ UPGRADE REQUIRED'}\n\n"
        
        # Tkinter
        tkinter_ok, tkinter_info = check_tkinter()
        system_report += f"Tkinter (GUI): {tkinter_info}\n"
        system_report += f"Status: {'✅ OK' if tkinter_ok else '❌ MISSING'}\n\n"
        
        # Project structure
        missing_files = check_project_structure()
        system_report += f"Project Files: {len(missing_files)} missing\n"
        if missing_files:
            system_report += "Missing files:\n"
            for file in missing_files:
                system_report += f"  • {file}\n"
            system_report += "Status: ❌ INCOMPLETE\n\n"
        else:
            system_report += "Status: ✅ COMPLETE\n\n"
        
        # Overall status
        all_ok = python_ok and tkinter_ok and not missing_files
        system_report += f"Overall Status: {'✅ READY TO RUN' if all_ok else '❌ ISSUES FOUND'}\n"
        
        self.system_text.insert(tk.END, system_report)
        
        # Dependencies check
        deps = check_optional_dependencies()
        deps_report = "📦 OPTIONAL DEPENDENCIES\n"
        deps_report += "=" * 30 + "\n\n"
        
        for dep, status in deps.items():
            deps_report += f"{dep}: {status}\n"
        
        deps_report += "\n💡 TIP: Install optional dependencies for the best experience:\n"
        deps_report += "pip install -r requirements_gui.txt\n"
        
        self.deps_text.insert(tk.END, deps_report)
        
        self.status_var.set("System check complete")
        
    def install_dependencies(self):
        """Install optional dependencies"""
        self.install_result.delete(1.0, tk.END)
        self.install_result.insert(tk.END, "Installing optional dependencies...\n")
        self.root.update()
        
        success = install_optional_dependencies()
        
        if success:
            self.install_result.insert(tk.END, "✅ Installation successful!\n")
            # Re-check dependencies
            deps = check_optional_dependencies()
            self.install_result.insert(tk.END, "\nUpdated status:\n")
            for dep, status in deps.items():
                self.install_result.insert(tk.END, f"{dep}: {status}\n")
        else:
            self.install_result.insert(tk.END, "❌ Installation failed. Check console for details.\n")
        
    def run_test(self):
        """Run GUI test"""
        self.test_result.delete(1.0, tk.END)
        self.test_result.insert(tk.END, "Running GUI test...\n")
        self.root.update()
        
        success, stdout, stderr = run_gui_test()
        
        if success:
            self.test_result.insert(tk.END, "✅ GUI test passed!\n")
            self.test_result.insert(tk.END, "The simulation is ready to run.\n\n")
        else:
            self.test_result.insert(tk.END, "❌ GUI test failed.\n")
            if stderr:
                self.test_result.insert(tk.END, f"Error: {stderr}\n")
        
        if stdout:
            self.test_result.insert(tk.END, f"Output:\n{stdout}\n")
            
    def launch_simulation(self):
        """Launch the main simulation"""
        try:
            subprocess.Popen([sys.executable, 'main_gui.py'])
            messagebox.showinfo("Launched", "Simulation launched in new window!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch simulation: {e}")
            
    def run(self):
        """Run the setup GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("🏰 Dwarf Fortress Simulation - Setup & Verification")
    print("=" * 50)
    
    # Check if we can run GUI
    try:
        import tkinter
        print("✅ Tkinter available - starting GUI setup...")
        app = SetupGUI()
        app.run()
    except ImportError:
        print("❌ Tkinter not available - running console setup...")
        
        # Console-based setup
        print("\nSystem Check:")
        python_ok, python_info = check_python_version()
        print(f"Python: {python_info} {'✅' if python_ok else '❌'}")
        
        tkinter_ok, tkinter_info = check_tkinter()
        print(f"Tkinter: {tkinter_info} {'✅' if tkinter_ok else '❌'}")
        
        missing_files = check_project_structure()
        print(f"Project Files: {'✅ Complete' if not missing_files else f'❌ {len(missing_files)} missing'}")
        
        deps = check_optional_dependencies()
        print("\nOptional Dependencies:")
        for dep, status in deps.items():
            print(f"  {dep}: {status}")
        
        if not python_ok or not tkinter_ok or missing_files:
            print("\n❌ System requirements not met. Please fix issues above.")
        else:
            print("\n✅ System ready! Run: python3 main_gui.py")

if __name__ == "__main__":
    main()
