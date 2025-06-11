# Contributing to Dwarf Fortress Simulation

Thank you for your interest in contributing to the Dwarf Fortress Simulation project! 

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/dwarf-fortress-simulation.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `python3 test_working.py`

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and return values
- Write descriptive docstrings for classes and functions
- Keep functions focused and modular

### Testing
- Run the test suite before submitting: `python3 test_working.py`
- Add tests for new features
- Ensure performance benchmarks still pass

### Architecture
- Follow the existing modular structure
- Use the Entity-Component-System pattern for new entities
- Add new AI behaviors in the `ai/` directory
- Extend world generation in `world/world_generator.py`

## Types of Contributions

### Bug Fixes
- Check existing issues first
- Include steps to reproduce
- Add test cases if applicable

### New Features
- Discuss major features in issues first
- Follow the existing architecture patterns
- Update documentation
- Add appropriate tests

### Performance Improvements
- Profile before and after changes
- Maintain the 60 FPS target with 100 entities
- Document performance impact

### Documentation
- Keep README.md up to date
- Add inline code comments
- Update IMPLEMENTATION_SUMMARY.md for major changes

## Submitting Changes

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes
3. Run tests: `python3 test_working.py`
4. Commit with descriptive messages
5. Push to your fork
6. Create a Pull Request

## Code Review Process

- All submissions require review
- Maintain backwards compatibility
- Ensure tests pass
- Follow the existing code style

## Questions?

Feel free to open an issue for questions or discussion!
