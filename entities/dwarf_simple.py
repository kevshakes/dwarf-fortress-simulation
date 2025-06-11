"""
Dwarf entity with AI, needs, and skills - simplified version
"""

import random
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from core.config import Constants

@dataclass
class DwarfStats:
    """Basic dwarf statistics"""
    strength: int = 10
    agility: int = 10
    intelligence: int = 10
    endurance: int = 10
    
class Dwarf:
    """Main dwarf entity class - simplified version"""
    
    def __init__(self, entity_id: int, position: Tuple[int, int, int], world_state):
        self.entity_id = entity_id
        self.entity_type = "dwarf"
        self.position = position
        self.world_state = world_state
        
        # Basic properties
        self.name = self._generate_name()
        self.age = random.randint(20, 150)
        self.stats = DwarfStats(
            strength=random.randint(8, 15),
            agility=random.randint(8, 15),
            intelligence=random.randint(8, 15),
            endurance=random.randint(8, 15)
        )
        
        # Needs system (0-100 scale)
        self.needs = {
            Constants.NEED_FOOD: random.randint(60, 90),
            Constants.NEED_DRINK: random.randint(60, 90),
            Constants.NEED_SLEEP: random.randint(60, 90),
            Constants.NEED_SOCIAL: random.randint(40, 80),
            Constants.NEED_WORK: random.randint(30, 70)
        }
        
        # Skills system (0-20 scale)
        self.skills = {
            Constants.SKILL_MINING: random.randint(0, 5),
            Constants.SKILL_CRAFTING: random.randint(0, 5),
            Constants.SKILL_COMBAT: random.randint(0, 3),
            Constants.SKILL_FARMING: random.randint(0, 3)
        }
        
        # Mood and personality
        self.mood = random.uniform(0.3, 0.8)  # 0-1 scale
        self.personality_traits = self._generate_personality()
        
        # Relationships (entity_id -> relationship_value)
        self.relationships: Dict[int, float] = {}
        
        # Inventory
        self.inventory: Dict[str, int] = {}
        self.max_carry_weight = 50
        self.current_carry_weight = 0
        
        # Current activity
        self.current_task = None
        self.task_progress = 0.0
        self.path_to_goal = []
        self.current_path_index = 0
        
        # Health and status
        self.health = 100
        self.stamina = 100
        self.is_sleeping = False
        self.is_working = False
        
        # Trauma and stress
        self.trauma_level = 0.0
        self.stress_level = random.uniform(0.1, 0.3)
        
    def _generate_name(self) -> str:
        """Generate a random dwarf name"""
        first_names = ["Thorin", "Balin", "Dwalin", "Fili", "Kili", "Dori", "Nori", "Ori", 
                      "Oin", "Gloin", "Bifur", "Bofur", "Bombur", "Gimli", "Groin", "Thrain"]
        last_names = ["Ironforge", "Stonebeard", "Goldaxe", "Deepdelver", "Mountainheart", 
                     "Rockbreaker", "Gemcutter", "Forgehammer", "Ironfoot", "Stormshield"]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
        
    def _generate_personality(self) -> Dict[str, float]:
        """Generate personality traits"""
        return {
            'hardworking': random.uniform(0.3, 1.0),
            'social': random.uniform(0.2, 0.9),
            'brave': random.uniform(0.1, 0.8),
            'creative': random.uniform(0.2, 0.8),
            'stubborn': random.uniform(0.3, 0.9)
        }
        
    def update(self, dt: float):
        """Update dwarf state"""
        # Decay needs over time
        self._update_needs(dt)
        
        # Update mood based on needs and environment
        self._update_mood(dt)
        
        # Update health and stamina
        self._update_health_stamina(dt)
        
        # Update stress and trauma
        self._update_stress_trauma(dt)
        
    def _update_needs(self, dt: float):
        """Update dwarf needs over time"""
        # Basic need decay rates (per second)
        decay_rates = {
            Constants.NEED_FOOD: 0.5,
            Constants.NEED_DRINK: 0.8,
            Constants.NEED_SLEEP: 0.3,
            Constants.NEED_SOCIAL: 0.2,
            Constants.NEED_WORK: 0.1
        }
        
        for need, rate in decay_rates.items():
            self.needs[need] = max(0, self.needs[need] - rate * dt)
            
        # Faster decay if working hard
        if self.is_working:
            self.needs[Constants.NEED_FOOD] = max(0, self.needs[Constants.NEED_FOOD] - 0.3 * dt)
            self.needs[Constants.NEED_DRINK] = max(0, self.needs[Constants.NEED_DRINK] - 0.5 * dt)
            
    def _update_mood(self, dt: float):
        """Update mood based on various factors"""
        # Base mood change
        mood_change = 0
        
        # Needs affect mood
        for need, value in self.needs.items():
            if value < 20:
                mood_change -= 0.1 * dt  # Very unhappy when needs are low
            elif value < 40:
                mood_change -= 0.05 * dt  # Somewhat unhappy
            elif value > 80:
                mood_change += 0.02 * dt  # Happy when needs are met
                
        # Environment affects mood
        temp = self.world_state.get_temperature(*self.position)
        if temp < Constants.TEMP_COLD:
            mood_change -= 0.03 * dt  # Cold makes dwarves unhappy
        elif temp > Constants.TEMP_HOT:
            mood_change -= 0.05 * dt  # Heat makes them more unhappy
            
        # Social interactions affect mood
        if self.needs[Constants.NEED_SOCIAL] > 60:
            mood_change += 0.01 * dt
            
        # Work satisfaction
        if self.is_working and self.needs[Constants.NEED_WORK] > 40:
            mood_change += 0.02 * dt
            
        # Apply mood change
        self.mood = max(0, min(1, self.mood + mood_change))
        
    def _update_health_stamina(self, dt: float):
        """Update health and stamina"""
        # Stamina recovery when not working
        if not self.is_working:
            self.stamina = min(100, self.stamina + 10 * dt)
        else:
            self.stamina = max(0, self.stamina - 5 * dt)
            
        # Health affected by needs
        if self.needs[Constants.NEED_FOOD] < 10:
            self.health = max(0, self.health - 2 * dt)  # Starving
        elif self.needs[Constants.NEED_DRINK] < 5:
            self.health = max(0, self.health - 5 * dt)  # Dehydrating
        else:
            # Slow health recovery when needs are met
            if all(need > 50 for need in self.needs.values()):
                self.health = min(100, self.health + 0.5 * dt)
                
    def _update_stress_trauma(self, dt: float):
        """Update stress and trauma levels"""
        # Stress increases with unmet needs
        stress_increase = 0
        for need, value in self.needs.items():
            if value < 30:
                stress_increase += 0.02 * dt
                
        # Trauma affects stress
        stress_increase += self.trauma_level * 0.01 * dt
        
        # Good mood reduces stress
        if self.mood > 0.7:
            stress_increase -= 0.01 * dt
            
        self.stress_level = max(0, min(1, self.stress_level + stress_increase))
        
        # Trauma slowly fades over time
        self.trauma_level = max(0, self.trauma_level - 0.001 * dt)
