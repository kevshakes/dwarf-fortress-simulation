"""
Entity Component System components
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Tuple

@dataclass
class PositionComponent:
    """Position in 3D space"""
    x: int
    y: int
    z: int

@dataclass
class MovementComponent:
    """Movement and velocity"""
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    velocity_z: float = 0.0
    max_speed: float = 5.0
    
@dataclass
class InventoryComponent:
    """Inventory storage"""
    items: Dict[str, int] = None
    max_weight: int = 50
    current_weight: int = 0
    
    def __post_init__(self):
        if self.items is None:
            self.items = {}

@dataclass
class SkillsComponent:
    """Skills and experience"""
    skills: Dict[str, int] = None
    experience: Dict[str, float] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = {}
        if self.experience is None:
            self.experience = {}

@dataclass
class NeedsComponent:
    """Basic needs"""
    food: float = 100.0
    drink: float = 100.0
    sleep: float = 100.0
    social: float = 50.0
    work: float = 50.0

@dataclass
class MoodComponent:
    """Mood and emotional state"""
    happiness: float = 0.5
    stress: float = 0.2
    trauma: float = 0.0
