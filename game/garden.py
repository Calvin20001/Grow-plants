"""
Garden Class
Manages the grid-based garden system and plant placement
"""

from typing import Dict, List, Optional, Tuple
from constants import *
from plant import Plant

class Garden:
    """Grid-based garden system for growing plants"""
    
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        
        # Grid system
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.plants = {}  # (x, y) -> Plant mapping
        
        # Garden state
        self.soil_quality = [[1.0 for _ in range(self.width)] for _ in range(self.height)]
        self.water_levels = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.fertilizer_levels = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Garden expansions
        self.expansions = 1
        self.max_expansions = 3
        
        # Weather effects
        self.rain_timer = 0.0
        self.pest_infestation = False
        self.pest_timer = 0.0
        
        # Initialize starting garden area
        self._initialize_garden()
    
    def _initialize_garden(self):
        """Initialize the starting garden area"""
        # Start with a 5x5 garden in the center
        start_x = (self.width // 2) - 2
        start_y = (self.height // 2) - 2
        
        for y in range(start_y, start_y + 5):
            for x in range(start_x, start_x + 5):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.soil_quality[y][x] = 1.0
                    self.water_levels[y][x] = 2
                    self.fertilizer_levels[y][x] = 0
    
    def update(self, dt: float):
        """Update garden state"""
        # Update all plants
        for plant in self.plants.values():
            plant.update(dt)
        
        # Update weather effects
        if self.rain_timer > 0:
            self.rain_timer -= dt
            if self.rain_timer <= 0:
                self._end_rain_effect()
        
        # Update pest infestation
        if self.pest_infestation:
            self.pest_timer += dt
            if self.pest_timer >= 30.0:  # Pests last 30 seconds
                self._end_pest_infestation()
    
    def plant_seed(self, x: int, y: int, seed_type: str) -> bool:
        """Plant a seed at the specified grid position"""
        if not self._is_valid_position(x, y):
            return False
        
        if self.grid[y][x] is not None:
            return False  # Position already occupied
        
        if not self._is_plantable_soil(x, y):
            return False  # Not plantable soil
        
        # Create new plant
        plant = Plant(seed_type, x, y)
        self.grid[y][x] = plant
        self.plants[(x, y)] = plant
        
        # Apply soil quality effects
        soil_quality = self.soil_quality[y][x]
        if soil_quality < 0.5:
            plant.growth_progress *= 0.8  # Slower growth on poor soil
        
        return True
    
    def water_plant(self, x: int, y: int) -> bool:
        """Water a plant at the specified position"""
        if not self._is_valid_position(x, y):
            return False
        
        plant = self.grid[y][x]
        if plant is None:
            return False
        
        # Water the plant
        if plant.water():
            # Update soil water level
            self.water_levels[y][x] = min(5, self.water_levels[y][x] + 1)
            return True
        
        return False
    
    def fertilize_plant(self, x: int, y: int) -> bool:
        """Apply fertilizer to a plant"""
        if not self._is_valid_position(x, y):
            return False
        
        plant = self.grid[y][x]
        if plant is None:
            return False
        
        # Apply fertilizer
        if plant.fertilize():
            # Update soil fertilizer level
            self.fertilizer_levels[y][x] = min(3, self.fertilizer_levels[y][x] + 1)
            return True
        
        return False
    
    def get_plant(self, x: int, y: int) -> Optional[Plant]:
        """Get plant at specified position"""
        if not self._is_valid_position(x, y):
            return None
        return self.grid[y][x]
    
    def remove_plant(self, x: int, y: int) -> bool:
        """Remove plant from specified position"""
        if not self._is_valid_position(x, y):
            return False
        
        if self.grid[y][x] is not None:
            plant = self.grid[y][x]
            del self.plants[(x, y)]
            self.grid[y][x] = None
            
            # Improve soil quality slightly when plant is harvested
            self.soil_quality[y][x] = min(1.5, self.soil_quality[y][x] + 0.1)
            
            return True
        
        return False
    
    def expand(self) -> bool:
        """Expand the garden area"""
        if self.expansions >= self.max_expansions:
            return False
        
        self.expansions += 1
        
        # Increase plantable area
        expansion_size = 2
        center_x = self.width // 2
        center_y = self.height // 2
        
        for y in range(center_y - expansion_size, center_y + expansion_size + 1):
            for x in range(center_x - expansion_size, center_x + expansion_size + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    if self.soil_quality[y][x] == 0:
                        self.soil_quality[y][x] = 0.8
                        self.water_levels[y][x] = 1
        
        return True
    
    def apply_rain_effect(self):
        """Apply rain effect to all plants"""
        self.rain_timer = 20.0  # Rain lasts 20 seconds
        
        # Water all plants
        for plant in self.plants.values():
            plant.water()
        
        # Increase soil water levels
        for y in range(self.height):
            for x in range(self.width):
                if self._is_plantable_soil(x, y):
                    self.water_levels[y][x] = min(5, self.water_levels[y][x] + 2)
    
    def _end_rain_effect(self):
        """End rain effect"""
        self.rain_timer = 0.0
    
    def trigger_pest_infestation(self):
        """Trigger pest infestation event"""
        if not self.pest_infestation:
            self.pest_infestation = True
            self.pest_timer = 0.0
            
            # Randomly destroy some plants
            import random
            plant_positions = list(self.plants.keys())
            if plant_positions:
                num_to_destroy = min(3, len(plant_positions))
                positions_to_destroy = random.sample(plant_positions, num_to_destroy)
                
                for x, y in positions_to_destroy:
                    self.remove_plant(x, y)
    
    def _end_pest_infestation(self):
        """End pest infestation"""
        self.pest_infestation = False
        self.pest_timer = 0.0
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within garden bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def _is_plantable_soil(self, x: int, y: int) -> bool:
        """Check if position has plantable soil"""
        return self.soil_quality[y][x] > 0
    
    def get_garden_summary(self) -> Dict:
        """Get summary of garden state"""
        return {
            "width": self.width,
            "height": self.height,
            "expansions": self.expansions,
            "max_expansions": self.max_expansions,
            "total_plants": len(self.plants),
            "plantable_tiles": sum(1 for row in self.soil_quality for quality in row if quality > 0),
            "weather": {
                "rain_timer": self.rain_timer,
                "pest_infestation": self.pest_infestation,
                "pest_timer": self.pest_timer
            }
        }
    
    def get_plant_positions(self) -> List[Tuple[int, int]]:
        """Get list of all plant positions"""
        return list(self.plants.keys())
    
    def get_plantable_positions(self) -> List[Tuple[int, int]]:
        """Get list of all plantable positions"""
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self._is_plantable_soil(x, y):
                    positions.append((x, y))
        return positions
