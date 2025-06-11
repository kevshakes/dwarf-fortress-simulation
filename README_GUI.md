# 🏰 Dwarf Fortress Simulation - GUI Version

A comprehensive dwarf fortress-style simulation with a user-friendly graphical interface built with Python Tkinter.

## 🎮 New GUI Features

### ✨ What's New in GUI Version
- **🖥️ Graphical Interface**: Full tkinter-based GUI with intuitive controls
- **🗺️ Interactive World View**: Click and drag to explore your world
- **🎛️ Control Panel**: Easy-to-use buttons and sliders for all settings
- **📊 Real-time Status**: Live performance and game statistics
- **🔧 Debug Tools**: Visual debug overlays and information panels
- **💾 Save/Load**: GUI file dialogs for managing save games
- **⚡ Performance**: Optimized for smooth 60 FPS GUI updates

### 🖱️ GUI Controls
- **Left Click**: Select tiles and entities
- **Right Click**: Context menus (coming soon)
- **Mouse Wheel**: Zoom in/out
- **Middle Click + Drag**: Pan the view
- **WASD Keys**: Move camera
- **Q/E Keys**: Change Z-levels

## 🚀 Quick Start - GUI Version

### 1. Test GUI Components
```bash
cd dwarf-fortress-simulation
python3 test_gui.py
```
This will open a test window to verify all GUI components work correctly.

### 2. Run Full GUI Simulation
```bash
python3 main_gui.py
```

### 3. Alternative: Command Line (Original)
```bash
python3 main.py --ascii --dwarves 5
```

## 📋 Installation

### Required (Included with Python)
- **Python 3.6+** with tkinter (standard library)

### Optional Dependencies
```bash
pip install -r requirements_gui.txt
```

**Optional packages provide:**
- `psutil`: Performance monitoring and memory usage
- `numpy`: Enhanced world generation (fallback available)
- `colorama`: Terminal colors for debug output

**The simulation works without optional dependencies!**

## 🎛️ GUI Interface Guide

### Main Window Layout
```
┌─────────────────────────────────────────────────────────────┐
│ File  Simulation  View  Help                    [Menu Bar] │
├─────────────────────────────────┬───────────────────────────┤
│                                 │ 🎛️ Controls              │
│                                 ├───────────────────────────┤
│         🗺️ World View          │ World Generation          │
│                                 │ • Size: [64x64]           │
│    Interactive map display      │ • Z-Levels: [15]          │
│    Click and drag to explore    │ • Dwarves: [7]            │
│                                 │ • [Generate World]        │
│                                 ├───────────────────────────┤
│                                 │ Simulation                │
│                                 │ ▶️ Start  ⏸️ Pause  ⏹️ Stop │
│                                 │ Speed: [====|====] 1.0x   │
│                                 ├───────────────────────────┤
│                                 │ 📊 Status                 │
│                                 │ FPS: 60.0                 │
│                                 │ Memory: 45.2 MB           │
│                                 │ Dwarves: 7                │
│                                 │ Entities: 127              │
├─────────────────────────────────┴───────────────────────────┤
│ Status: Simulation running - 60 FPS                        │
└─────────────────────────────────────────────────────────────┘
```

### Menu Options

#### 📁 File Menu
- **New World**: Generate a new procedural world
- **Load World**: Load a saved game file
- **Save World**: Save current game state
- **Exit**: Close the application

#### ⚡ Simulation Menu
- **Start**: Begin the simulation
- **Pause**: Pause/resume simulation
- **Stop**: Stop simulation completely
- **Speed Up/Down**: Adjust simulation speed

#### 👁️ View Menu
- **Zoom In/Out**: Adjust world view zoom
- **Reset View**: Center camera on world
- **Show Debug Info**: Toggle debug panels

#### ❓ Help Menu
- **Controls**: Show control help
- **About**: Application information

### 🎛️ Control Panel Features

#### World Generation
- **World Size**: 32x32 to 128x128 tiles
- **Z-Levels**: 5 to 30 vertical layers
- **Dwarves**: 1 to 20 initial population
- **Debug Mode**: Enable development features

#### Simulation Controls
- **Play/Pause/Stop**: Standard media controls
- **Speed Slider**: 0.1x to 3.0x simulation speed
- **Real-time Status**: FPS, memory, entity counts

#### View Controls
- **Camera Movement**: Arrow buttons for precise control
- **Z-Level**: Up/Down buttons for vertical navigation
- **Zoom**: In/Out buttons with reset option

### 📊 Status Panel

#### Performance Metrics
- **FPS**: Real-time frame rate
- **Memory**: Current memory usage
- **Entity Count**: Total active entities

#### World Information
- **World Size**: Current world dimensions
- **Z-Levels**: Vertical layers
- **Current Year**: Simulation time

#### Population Stats
- **Dwarves**: Active dwarf count
- **Total Entities**: All game objects

### 🔧 Debug Panel (Optional)

#### Debug Toggles
- **Show Pathfinding**: Visualize AI pathfinding
- **Show AI Decisions**: Display dwarf decision making
- **Show Resource Flows**: Highlight resource movement

#### Debug Information
- **Real-time Debug Log**: Scrolling debug output
- **Performance Metrics**: Detailed timing information
- **System Status**: Component health monitoring

## 🎮 How to Play

### 1. Generate a World
1. Adjust world parameters in the Control Panel
2. Click "🌍 Generate World"
3. Wait for world generation to complete

### 2. Start the Simulation
1. Click "▶️ Start" in the Simulation controls
2. Watch your dwarves come to life!
3. Use the View controls to explore

### 3. Monitor Progress
- Check the Status panel for performance
- Watch dwarves in the World View
- Use Debug panel for detailed information

### 4. Save Your Progress
- Use File → Save World to preserve your game
- Load saved worlds with File → Load World

## 🔧 Troubleshooting

### GUI Won't Start
```bash
# Test GUI components first
python3 test_gui.py

# Check Python tkinter installation
python3 -c "import tkinter; print('Tkinter OK')"
```

### Performance Issues
- Reduce world size (32x32 instead of 128x128)
- Lower Z-levels (10 instead of 20)
- Fewer initial dwarves (3-5 instead of 10+)
- Close debug panels when not needed

### Missing Features
- Install optional dependencies: `pip install -r requirements_gui.txt`
- Some features gracefully degrade without dependencies

## 🆚 GUI vs Command Line

| Feature | GUI Version | Command Line |
|---------|-------------|--------------|
| **Ease of Use** | ✅ Point & Click | ⚠️ Commands |
| **Visual World** | ✅ Interactive Map | ⚠️ ASCII Art |
| **Real-time Control** | ✅ Buttons & Sliders | ⚠️ Keyboard Only |
| **Debug Tools** | ✅ Visual Panels | ✅ Text Output |
| **Performance** | ✅ 60 FPS GUI | ✅ 60 FPS Simulation |
| **Save/Load** | ✅ File Dialogs | ✅ Command Args |
| **Accessibility** | ✅ User Friendly | ⚠️ Technical Users |

## 🔮 Future GUI Enhancements

### Planned Features
- **🏗️ Construction Mode**: Click to build structures
- **👥 Dwarf Management**: Individual dwarf panels
- **📈 Statistics Graphs**: Visual performance charts
- **🎨 Themes**: Dark/light mode options
- **🔊 Sound Effects**: Audio feedback (optional)
- **📱 Responsive Design**: Better window resizing

### Advanced Features
- **🗺️ Mini-map**: Overview of entire world
- **📋 Task Management**: Assign jobs to dwarves
- **💰 Economy Panel**: Resource management interface
- **🏛️ Diplomacy**: Interaction with other civilizations

## 📞 Support

### Getting Help
1. **Test GUI**: Run `python3 test_gui.py` first
2. **Check Console**: Look for error messages
3. **Verify Installation**: Ensure all files are present
4. **Report Issues**: Use GitHub issues for bugs

### Common Solutions
- **Import Errors**: Check file structure and Python path
- **GUI Freezing**: Reduce world size or entity count
- **Slow Performance**: Install optional dependencies
- **Save/Load Issues**: Check file permissions

## 🎉 Success!

You now have a fully functional GUI version of the Dwarf Fortress Simulation! 

**Enjoy exploring your procedurally generated worlds with an intuitive graphical interface!** 🏰⚒️
