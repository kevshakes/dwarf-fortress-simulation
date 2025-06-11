"""
Historical timeline and civilization generator
"""

import random
from typing import List
from world.world_state import HistoricalEvent

class HistoryGenerator:
    """Generates historical events and civilizations"""
    
    def __init__(self, seed: int):
        self.seed = seed
        random.seed(seed)
        
    def generate_history(self, world_state) -> List[HistoricalEvent]:
        """Generate historical timeline"""
        events = []
        
        # Generate some basic historical events
        for year in range(-500, 0):  # 500 years of history
            if random.random() < 0.1:  # 10% chance per year
                event = self._generate_random_event(year)
                events.append(event)
                
        return events
        
    def _generate_random_event(self, year: int) -> HistoricalEvent:
        """Generate a random historical event"""
        event_types = [
            "settlement_founded",
            "trade_route_established", 
            "natural_disaster",
            "discovery",
            "conflict"
        ]
        
        event_type = random.choice(event_types)
        descriptions = {
            "settlement_founded": "A new settlement was established",
            "trade_route_established": "A trade route was opened",
            "natural_disaster": "A natural disaster struck the region",
            "discovery": "A significant discovery was made",
            "conflict": "A conflict arose between groups"
        }
        
        return HistoricalEvent(
            year=year,
            event_type=event_type,
            description=descriptions[event_type]
        )
