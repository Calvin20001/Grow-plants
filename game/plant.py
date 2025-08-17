"""
Plant Class
Handles individual plant growth, mutations, and states
"""

import random
import time
from typing import Dict, Optional
from constants import *

class Plant:
    """Individual plant with growth stages and mutations"""
    
    def __init__(self, plant_type: str, x: int, y: int):
        self.plant_type = plant_type
        self.x = x
        self.y = y
        
        # Get plant data from constants
        plant_data = PLANT_TYPES.get(plant_type, PLANT_TYPES["carrot"])
        self.name = plant_data["name"]
        self.base_growth_time = plant_data["growth_time"]
        self.water_need = plant_data["water_need"]
        self.base_value = plant_data["base_value"]
        self.base_mutation_chance = plant_data["mutation_chance"]
        self.base_color = plant_data["color"]
        
        # Growth state
        self.current_stage = 0  # Index into GROWTH_STAGES
        self.growth_progress = 0.0  # 0.0 to 1.0
        self.growth_timer = 0.0
        self.stage_timer = 0.0
        
        # Water and care
        self.water_level = 0
        self.max_water_level = self.water_need
        self.last_watered = 0.0
        self.fertilized = False
        
        # Mutations
        self.mutations = []
        self.is_mutated = False
        self.mutation_multiplier = 1.0
        
        # Visual properties
        self.size_multiplier = 1.0
        self.color_variants = []
        
        # Check for initial mutation
        self._check_initial_mutation()
    
    def update(self, dt: float):
        """Update plant growth"""
        self.growth_timer += dt
        self.stage_timer += dt
        
        # Calculate growth rate
        growth_rate = self._calculate_growth_rate()
        
        # Update growth progress
        self.growth_progress += growth_rate * dt
        
        # Check for stage advancement
        if self.growth_progress >= 1.0 and self.current_stage < len(GROWTH_STAGES) - 1:
            self._advance_stage()
        
        # Reduce water over time
        if self.growth_timer - self.last_watered > 10.0:  # Water depletes every 10 seconds
            self.water_level = max(0, self.water_level - 1)
    
    def _calculate_growth_rate(self) -> float:
        """Calculate current growth rate based on conditions"""
        base_rate = 1.0 / self.base_growth_time
        
        # Water bonus
        water_bonus = 1.0
        if self.water_level >= self.max_water_level:
            water_bonus = 1.0 + WATERING_BONUS
        elif self.water_level == 0:
            water_bonus = 0.5  # Slow growth when dry
        
        # Fertilizer bonus
        fertilizer_bonus = 1.0 + FERTILIZER_BONUS if self.fertilized else 1.0
        
        return base_rate * water_bonus * fertilizer_bonus
    
    def _advance_stage(self):
        """Advance to next growth stage"""
        self.current_stage += 1
        self.growth_progress = 0.0
        self.stage_timer = 0.0
        
        # Check for mutations on stage advancement
        if self.current_stage > 1:  # Don't mutate on seed stage
            self._check_mutation()
    
    def _check_initial_mutation(self):
        """Check for initial mutation when planted"""
        if random.random() < self.base_mutation_chance * 0.1:  # Lower chance for initial
            self._apply_mutation("early_growth")
    
    def _check_mutation(self):
        """Check for mutations during growth"""
        if self.is_mutated:
            return  # Already mutated
        
        mutation_chance = self.base_mutation_chance
        
        # Increase chance with fertilizer
        if self.fertilized:
            mutation_chance *= 1.5
        
        # Increase chance with good care
        if self.water_level >= self.max_water_level:
            mutation_chance *= 1.2
        
        if random.random() < mutation_chance:
            self._apply_mutation("growth_spurt")
    
    def _apply_mutation(self, mutation_type: str):
        """Apply a mutation to the plant"""
        self.is_mutated = True
        self.mutations.append(mutation_type)
        
        if mutation_type == "growth_spurt":
            self.mutation_multiplier = 1.5
            self.size_multiplier = 1.3
        elif mutation_type == "early_growth":
            self.mutation_multiplier = 1.2
            self.growth_progress += 0.3
        elif mutation_type == "rare_color":
            self.color_variants.append("rare")
            self.mutation_multiplier = 2.0
        elif mutation_type == "giant":
            self.size_multiplier = 2.0
            self.mutation_multiplier = 3.0
    
    def water(self) -> bool:
        """Water the plant"""
        if self.water_level < self.max_water_level:
            self.water_level = min(self.max_water_level, self.water_level + 1)
            self.last_watered = self.growth_timer
            return True
        return False
    
    def fertilize(self) -> bool:
        """Apply fertilizer to the plant"""
        if not self.fertilized:
            self.fertilized = True
            return True
        return False
    
    def get_current_stage(self) -> str:
        """Get current growth stage name"""
        return GROWTH_STAGES[self.current_stage]
    
    def is_harvestable(self) -> bool:
        """Check if plant is ready for harvest"""
        return self.current_stage == len(GROWTH_STAGES) - 1
    
    def get_value(self) -> int:
        """Calculate plant's current value"""
        base_value = self.base_value
        
        # Stage multiplier
        stage_multiplier = 1.0 + (self.current_stage * 0.2)
        
        # Mutation multiplier
        mutation_multiplier = self.mutation_multiplier
        
        # Care bonus
        care_bonus = 1.0
        if self.fertilized:
            care_bonus += 0.3
        if self.water_level >= self.max_water_level:
            care_bonus += 0.2
        
        return int(base_value * stage_multiplier * mutation_multiplier * care_bonus)
    
    def get_visual_properties(self) -> Dict:
        """Get visual properties for rendering"""
        stage = self.get_current_stage()
        
        # Base size based on stage
        base_size = 0.3 + (self.current_stage * 0.15)
        final_size = base_size * self.size_multiplier
        
        # Color variations
        color = self.base_color
        if "rare" in self.color_variants:
            color = PURPLE  # Rare color
        
        return {
            "size": final_size,
            "color": color,
            "stage": stage,
            "water_level": self.water_level,
            "max_water_level": self.max_water_level,
            "fertilized": self.fertilized,
            "mutated": self.is_mutated
        }
    
    def get_status_summary(self) -> Dict:
        """Get summary of plant status"""
        return {
            "type": self.plant_type,
            "name": self.name,
            "stage": self.get_current_stage(),
            "growth_progress": self.growth_progress,
            "water_level": self.water_level,
            "max_water_level": self.max_water_level,
            "fertilized": self.fertilized,
            "mutated": self.is_mutated,
            "mutations": self.mutations.copy(),
            "value": self.get_value(),
            "position": (self.x, self.y)
        }
