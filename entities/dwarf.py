"""
Dwarf entity with AI, needs, and skills
"""

import random
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from core.config import Constants
from world.world_state import WorldState

@dataclass
class DwarfStats:
    """Basic dwarf statistics"""
    strength: int = 10
    agility: int = 10
    intelligence: int = 10
    endurance: int = 10
    
class Dwarf:
    """Main dwarf entity class"""
    
    def __init__(self, entity_id: int, position: Tuple[int, int, int], world_state: WorldState):
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
        tile = self.world_state.get_tile(*self.position)
        if tile.temperature < Constants.TEMP_COLD:
            mood_change -= 0.03 * dt  # Cold makes dwarves unhappy
        elif tile.temperature > Constants.TEMP_HOT:
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
        
    def add_trauma(self, amount: float):
        """Add trauma from witnessing events"""
        self.trauma_level = min(1, self.trauma_level + amount)
        
    def gain_skill_experience(self, skill: str, amount: float):
        """Gain experience in a skill"""
        if skill in self.skills:
            # Experience required increases with skill level
            required_exp = (self.skills[skill] + 1) * 10
            current_exp = getattr(self, f"{skill}_exp", 0)
            current_exp += amount
            
            if current_exp >= required_exp:
                self.skills[skill] += 1
                current_exp = 0
                print(f"{self.name} gained a level in {skill}! Now level {self.skills[skill]}")
                
            setattr(self, f"{skill}_exp", current_exp)
            
    def can_perform_task(self, task_type: str, required_skill_level: int = 0) -> bool:
        """Check if dwarf can perform a specific task"""
        if task_type in self.skills:
            return self.skills[task_type] >= required_skill_level
        return False
        
    def add_relationship(self, other_dwarf_id: int, relationship_change: float):
        """Modify relationship with another dwarf"""
        if other_dwarf_id not in self.relationships:
            self.relationships[other_dwarf_id] = 0.0
            
        self.relationships[other_dwarf_id] = max(-1, min(1, 
            self.relationships[other_dwarf_id] + relationship_change))
            
    def get_relationship(self, other_dwarf_id: int) -> float:
        """Get relationship value with another dwarf"""
        return self.relationships.get(other_dwarf_id, 0.0)
        
    def add_item(self, item_type: str, quantity: int = 1) -> bool:
        """Add item to inventory if there's space"""
        # Simple weight check (each item weighs 1 unit for now)
        if self.current_carry_weight + quantity <= self.max_carry_weight:
            self.inventory[item_type] = self.inventory.get(item_type, 0) + quantity
            self.current_carry_weight += quantity
            return True
        return False
        
    def remove_item(self, item_type: str, quantity: int = 1) -> int:
        """Remove item from inventory, return actual amount removed"""
        if item_type in self.inventory:
            actual_removed = min(quantity, self.inventory[item_type])
            self.inventory[item_type] -= actual_removed
            self.current_carry_weight -= actual_removed
            
            if self.inventory[item_type] <= 0:
                del self.inventory[item_type]
                
            return actual_removed
        return 0
        
    def has_item(self, item_type: str, quantity: int = 1) -> bool:
        """Check if dwarf has specified item and quantity"""
        return self.inventory.get(item_type, 0) >= quantity
        
    def serialize(self) -> Dict[str, Any]:
        """Serialize dwarf for saving"""
        return {
            'type': 'dwarf',
            'entity_id': self.entity_id,
            'position': self.position,
            'name': self.name,
            'age': self.age,
            'stats': {
                'strength': self.stats.strength,
                'agility': self.stats.agility,
                'intelligence': self.stats.intelligence,
                'endurance': self.stats.endurance
            },
            'needs': self.needs.copy(),
            'skills': self.skills.copy(),
            'mood': self.mood,
            'personality_traits': self.personality_traits.copy(),
            'relationships': self.relationships.copy(),
            'inventory': self.inventory.copy(),
            'health': self.health,
            'stamina': self.stamina,
            'trauma_level': self.trauma_level,
            'stress_level': self.stress_level
        }
        
    @classmethod
    def deserialize(cls, data: Dict[str, Any], world_state: WorldState) -> 'Dwarf':
        """Deserialize dwarf from save data"""
        dwarf = cls(data['entity_id'], tuple(data['position']), world_state)
        
        dwarf.name = data['name']
        dwarf.age = data['age']
        dwarf.stats = DwarfStats(**data['stats'])
        dwarf.needs = data['needs']
        dwarf.skills = data['skills']
        dwarf.mood = data['mood']
        dwarf.personality_traits = data['personality_traits']
        dwarf.relationships = data['relationships']
        dwarf.inventory = data['inventory']
        dwarf.health = data['health']
        dwarf.stamina = data['stamina']
        dwarf.trauma_level = data['trauma_level']
        dwarf.stress_level = data['stress_level']
        
        return dwarf
