#!/usr/bin/env python3
"""
Universal launcher for Dwarf Fortress Simulation
Automatically detects the best way to run the simulation
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

def check_gui_available():
    """Check if GUI is available"""
    try:
        import tkinter
        import tkinter.ttk
        return True
    except ImportError:
        return False

def check_dependencies():
    """Check what dependencies are available"""
    deps = {
        'tkinter': False,
        'psutil': False,
        'numpy': False,
        'colorama': False
    }
    
    try:
        import tkinter
        deps['tkinter'] = True
    except ImportError:
        pass
    
    try:
        import psutil
        deps['psutil'] = True
    except ImportError:
        pass
    
    try:
        import numpy
        deps['numpy'] = True
    except ImportError:
        pass
    
    try:
        import colorama
        deps['colorama'] = True
    except ImportError:
        pass
    
    return deps

class LauncherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏰 Dwarf Fortress Simulation Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.deps = check_dependencies()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the launcher UI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, text="🏰 Dwarf Fortress Simulation", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(title_frame, text="Choose how to run the simulation", 
                                 font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack(pady=(0, 15))
        
        # Main content
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Launch options
        options_frame = ttk.LabelFrame(main_frame, text="Launch Options", padding=15)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # GUI option
        gui_frame = tk.Frame(options_frame)
        gui_frame.pack(fill=tk.X, pady=5)
        
        gui_status = "✅ Available" if self.deps['tkinter'] else "❌ Not Available"
        ttk.Button(gui_frame, text="🖥️ GUI Version (Recommended)", 
                  command=self.launch_gui, 
                  state="normal" if self.deps['tkinter'] else "disabled").pack(side=tk.LEFT)
        tk.Label(gui_frame, text=gui_status, fg='green' if self.deps['tkinter'] else 'red').pack(side=tk.RIGHT)
        
        # Command line option
        cli_frame = tk.Frame(options_frame)
        cli_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(cli_frame, text="💻 Command Line Version", 
                  command=self.launch_cli).pack(side=tk.LEFT)
        tk.Label(cli_frame, text="✅ Always Available").pack(side=tk.RIGHT)
        
        # Test option
        test_frame = tk.Frame(options_frame)
        test_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(test_frame, text="🧪 Test GUI Components", 
                  command=self.launch_test,
                  state="normal" if self.deps['tkinter'] else "disabled").pack(side=tk.LEFT)
        tk.Label(test_frame, text="🔧 Diagnostic Tool").pack(side=tk.RIGHT)
        
        # Setup option
        setup_frame = tk.Frame(options_frame)
        setup_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(setup_frame, text="⚙️ Setup & Install Dependencies", 
                  command=self.launch_setup,
                  state="normal" if self.deps['tkinter'] else "disabled").pack(side=tk.LEFT)
        tk.Label(setup_frame, text="📦 Installation Helper").pack(side=tk.RIGHT)
        
        # System status
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        status_text = f"""
Python Version: {sys.version.split()[0]} ✅
GUI Framework (tkinter): {'✅ Available' if self.deps['tkinter'] else '❌ Missing'}
Performance Monitor (psutil): {'✅ Installed' if self.deps['psutil'] else '⚠️ Optional'}
Enhanced Generation (numpy): {'✅ Installed' if self.deps['numpy'] else '⚠️ Optional'}
Terminal Colors (colorama): {'✅ Installed' if self.deps['colorama'] else '⚠️ Optional'}

Recommendation: {'🎉 Ready for GUI!' if self.deps['tkinter'] else '💻 Command line only'}
        """
        
        status_label = tk.Label(status_frame, text=status_text, justify=tk.LEFT, font=('Courier', 9))
        status_label.pack()
        
        # Quick start info
        info_frame = ttk.LabelFrame(main_frame, text="Quick Start", padding=15)
        info_frame.pack(fill=tk.X)
        
        if self.deps['tkinter']:
            info_text = "🚀 Click 'GUI Version' above for the best experience!\n\nThe GUI provides:\n• Interactive world view\n• Easy controls\n• Real-time statistics\n• Visual debugging tools"
        else:
            info_text = "💻 GUI not available. Use Command Line version.\n\nTo enable GUI:\n1. Install tkinter (usually included with Python)\n2. Run setup to install optional dependencies\n3. Restart this launcher"
        
        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
        
    def launch_gui(self):
        """Launch GUI version"""
        try:
            subprocess.Popen([sys.executable, 'main_gui.py'])
            messagebox.showinfo("Launched", "GUI version launched!")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch GUI: {e}")
            
    def launch_cli(self):
        """Launch command line version"""
        try:
            # Show CLI options dialog
            cli_window = tk.Toplevel(self.root)
            cli_window.title("Command Line Options")
            cli_window.geometry("400x300")
            
            tk.Label(cli_window, text="Command Line Launch Options", 
                    font=('Arial', 12, 'bold')).pack(pady=10)
            
            options = [
                ("Basic simulation (5 dwarves)", ["--ascii", "--dwarves", "5"]),
                ("Debug mode (3 dwarves)", ["--debug", "--ascii", "--dwarves", "3"]),
                ("Stress test (many entities)", ["--generate", "stress_test"]),
                ("Performance benchmark", ["--generate", "benchmark"]),
                ("Custom world (10 dwarves)", ["--world-size", "64", "--dwarves", "10", "--ascii"])
            ]
            
            for desc, args in options:
                btn = ttk.Button(cli_window, text=desc, 
                               command=lambda a=args: self.run_cli_with_args(a))
                btn.pack(pady=5, padx=20, fill=tk.X)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show CLI options: {e}")
            
    def run_cli_with_args(self, args):
        """Run CLI with specific arguments"""
        try:
            subprocess.Popen([sys.executable, 'main.py'] + args)
            messagebox.showinfo("Launched", f"Command line version launched with: {' '.join(args)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch CLI: {e}")
            
    def launch_test(self):
        """Launch GUI test"""
        try:
            subprocess.Popen([sys.executable, 'test_gui.py'])
            messagebox.showinfo("Launched", "GUI test launched!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch test: {e}")
            
    def launch_setup(self):
        """Launch setup tool"""
        try:
            subprocess.Popen([sys.executable, 'setup_gui.py'])
            messagebox.showinfo("Launched", "Setup tool launched!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch setup: {e}")
            
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

def console_launcher():
    """Console-based launcher for when GUI is not available"""
    print("🏰 Dwarf Fortress Simulation - Console Launcher")
    print("=" * 50)
    
    deps = check_dependencies()
    
    print("System Status:")
    print(f"  Python: {sys.version.split()[0]} ✅")
    print(f"  GUI (tkinter): {'✅' if deps['tkinter'] else '❌'}")
    print(f"  Performance (psutil): {'✅' if deps['psutil'] else '⚠️'}")
    print(f"  Enhanced (numpy): {'✅' if deps['numpy'] else '⚠️'}")
    print(f"  Colors (colorama): {'✅' if deps['colorama'] else '⚠️'}")
    
    print("\nAvailable Options:")
    print("1. Run basic simulation (ASCII mode)")
    print("2. Run with debug mode")
    print("3. Run stress test")
    print("4. Run performance benchmark")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                subprocess.run([sys.executable, 'main.py', '--ascii', '--dwarves', '5'])
                break
            elif choice == '2':
                subprocess.run([sys.executable, 'main.py', '--debug', '--ascii', '--dwarves', '3'])
                break
            elif choice == '3':
                subprocess.run([sys.executable, 'main.py', '--generate', 'stress_test'])
                break
            elif choice == '4':
                subprocess.run([sys.executable, 'main.py', '--generate', 'benchmark'])
                break
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    if check_gui_available():
        # Use GUI launcher
        app = LauncherGUI()
        app.run()
    else:
        # Use console launcher
        console_launcher()

if __name__ == "__main__":
    main()
