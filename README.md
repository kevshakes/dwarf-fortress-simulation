# Dwarf Fortress-Style Simulation

A comprehensive dwarf fortress-style simulation game with procedural world generation, AI-driven dwarf agents, resource management, and multi-layer physics simulation.

## Features

### Core Systems
- **Procedural World Generation**: 3D Perlin noise terrain generation with biome classification, mineral veins, and historical timeline
- **Modular AI System**: Dwarf agents with needs hierarchy, A* pathfinding, skill progression, relationships, and mood system
- **Resource Management**: Flow-based inventory, production chains (ore → metal → tools), stockpile allocation, and temperature-aware food decay
- **Multi-layer Simulation**: Z-level fluid dynamics, heat propagation, mining collapse detection, and entity-component architecture

### Performance Optimizations
- Spatial partitioning for efficient entity queries
- Pathfinding cache system
- Delta-time simulation for consistent performance
- Target: 60 FPS with 100 agents, <2GB memory usage

### Debug Features
- ASCII rendering with fallback mode
- Debug overlays for pathfinding, AI decisions, and resource flows
- Performance monitoring and statistics
- CLI commands for debugging and optimization

## Installation

1. Install Python 3.6+ and required packages:
```bash
pip install -r requirements.txt
```

2. Run the simulation:
```bash
python main.py
```

## CLI Commands

### Debug Commands
- `--debug`: Enable debug mode
- `--ascii`: Use ASCII rendering mode
- `--debug-pathfinding`: Show pathfinding visualization

### Optimization Commands
- `--optimize spatial_partitioning grid_size=64`: Optimize spatial partitioning
- `--optimize pathfinding_cache`: Manage pathfinding cache

### Scenario Generation
- `--generate test_scenario 10_dwarves`: Generate test scenario with specified dwarf count
- `--generate stress_test`: Create maximum entities for stress testing
- `--generate benchmark`: Run performance benchmark

## Game Controls

- **WASD**: Move camera
- **QE**: Change Z-level
- **R**: Reset camera view
- **ESC**: Quit simulation

## Architecture

### Core Components
- `GameEngine`: Main game loop and system coordination
- `WorldGenerator`: Procedural world generation using 3D Perlin noise
- `EntityManager`: Entity-Component-System architecture
- `AIManager`: Coordinates all AI systems
- `ResourceManager`: Handles resource flows and production chains
- `PhysicsEngine`: Multi-layer physics simulation
- `Renderer`: ASCII rendering with debug overlays

### AI Systems
- `AStarPathfinder`: 3D pathfinding with z-level navigation
- `DwarfAI`: Individual dwarf behavior controller
- `NeedsSystem`: Manages dwarf needs and their effects
- `RelationshipSystem`: Handles dwarf-to-dwarf relationships
- `DecisionTree`: Makes AI decisions based on current state

### Resource Systems
- `StockpileManager`: Manages resource storage locations
- `ProductionManager`: Handles production chains and queues
- `ResourceFlow`: Flow-based resource movement system

## World Generation

The world is generated using 3D Perlin noise with multiple layers:
- **Terrain**: Stone, soil, and empty space distribution
- **Biomes**: Mountain, forest, desert, swamp classification
- **Minerals**: Iron, copper, gold, silver, coal veins
- **Water Features**: Rivers, lakes, underground water
- **Temperature**: Depth-based temperature with magma layers
- **History**: Procedural historical events and civilization spread

## Dwarf AI

Each dwarf has:
- **Needs**: Food, drink, sleep, social, work (0-100 scale)
- **Skills**: Mining, crafting, combat, farming (0-20 scale)
- **Mood**: Affected by needs, environment, and social interactions
- **Relationships**: Dynamic relationship matrix with other dwarves
- **Personality**: Traits affecting behavior and decision making
- **Health**: Affected by needs fulfillment and environmental factors

## Performance Features

- **Spatial Partitioning**: Grid-based entity organization for O(1) neighbor queries
- **Pathfinding Cache**: LRU cache for frequently used paths
- **Delta-time Simulation**: Consistent simulation regardless of framerate
- **Memory Management**: Compressed save/load system
- **Performance Monitoring**: Real-time FPS, memory, and CPU tracking

## Save System

- Compressed save files using gzip and pickle
- Metadata tracking (version, timestamp, compression status)
- Save file management (list, delete, backup, info export)
- Automatic save validation and error handling

## Extending the System

The modular architecture supports easy extension:
- Add new AI behaviors in `ai/` directory
- Create new resource types in `resources/item.py`
- Add production chains in `resources/production_chain.py`
- Implement new world generation features in `world/world_generator.py`
- Add new entity components in `entities/components.py`

## Debug and Development

Use the CLI debug commands for development:
```bash
# Enable pathfinding visualization
python main.py --debug --debug-pathfinding

# Run stress test
python main.py --generate stress_test

# Optimize spatial partitioning
python main.py --optimize spatial_partitioning grid_size=32

# Run benchmark
python main.py --generate benchmark
```

## Future Expansion

The system is designed to support future features:
- Magic systems
- Political systems
- Artifact generation
- Advanced combat
- Trade and diplomacy
- Weather and seasons
- Advanced crafting trees

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.
