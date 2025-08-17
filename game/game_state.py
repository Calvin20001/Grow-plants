"""
Game State Management
Handles all game data, player progress, and world state
"""

import time
from typing import Dict, List, Optional
from constants import *
from player import Player
from garden import Garden
from shop import Shop
from economy import Economy

class GameState:
    """Main game state manager"""
    
    def __init__(self):
        self.current_state = STATE_PLAYING
        self.game_time = 0.0
        self.day = 1
        
        # Core systems
        self.player = Player()
        self.garden = Garden()
        self.shop = Shop()
        self.economy = Economy()
        
        # Game progression
        self.unlocked_plants = ["carrot"]
        self.unlocked_tools = ["basic_watering_can"]
        self.garden_expansions = 1
        
        # Weather and events
        self.weather = "sunny"
        self.weather_timer = 0.0
        self.active_events = []
        
        # Statistics
        self.plants_harvested = 0
        self.total_earnings = 0
        self.mutations_found = 0
        
    def update(self, dt: float):
        """Update game state"""
        self.game_time += dt
        self.weather_timer += dt
        
        # Update systems
        self.player.update(dt)
        self.garden.update(dt)
        self.economy.update(dt)
        
        # Update weather (every 30 seconds)
        if self.weather_timer >= 30.0:
            self._update_weather()
            self.weather_timer = 0.0
            
        # Check for day change (every 5 minutes)
        if self.game_time >= 300.0:
            self.day += 1
            self.game_time = 0.0
            self._start_new_day()
    
    def _update_weather(self):
        """Update weather conditions"""
        import random
        
        weather_chances = {
            "sunny": 0.6,
            "cloudy": 0.25,
            "rainy": 0.15
        }
        
        rand = random.random()
        cumulative = 0
        for weather, chance in weather_chances.items():
            cumulative += chance
            if rand <= cumulative:
                self.weather = weather
                break
    
    def _start_new_day(self):
        """Handle new day events"""
        # Market fluctuations
        self.economy.update_market_prices()
        
        # Random events
        self._check_random_events()
    
    def _check_random_events(self):
        """Check for random events"""
        import random
        
        # Rainstorm (free watering)
        if self.weather == "rainy" and random.random() < 0.3:
            self.garden.apply_rain_effect()
            
        # Market boom (price increase)
        if random.random() < 0.1:
            self.economy.trigger_market_boom()
            
        # Pest infestation
        if random.random() < 0.05:
            self.garden.trigger_pest_infestation()
    
    def get_player_position(self):
        """Get current player position"""
        return self.player.x, self.player.y
    
    def can_afford(self, cost: int) -> bool:
        """Check if player can afford an item"""
        return self.economy.money >= cost
    
    def purchase_item(self, item_type: str, item_name: str) -> bool:
        """Purchase an item from the shop"""
        item = self.shop.get_item(item_type, item_name)
        if not item:
            return False
            
        if self.can_afford(item["cost"]):
            self.economy.spend_money(item["cost"])
            
            if item_type == "seed":
                self.player.add_seed(item_name)
            elif item_type == "tool":
                self.player.add_tool(item_name)
            elif item_type == "expansion":
                self.garden_expansions += 1
                self.garden.expand()
                
            return True
        return False
    
    def plant_seed(self, x: int, y: int, seed_type: str) -> bool:
        """Plant a seed in the garden"""
        if self.player.has_seed(seed_type):
            if self.garden.plant_seed(x, y, seed_type):
                self.player.use_seed(seed_type)
                return True
        return False
    
    def water_plant(self, x: int, y: int) -> bool:
        """Water a plant in the garden"""
        return self.garden.water_plant(x, y)
    
    def harvest_plant(self, x: int, y: int) -> bool:
        """Harvest a plant from the garden"""
        plant = self.garden.get_plant(x, y)
        if plant and plant.is_harvestable():
            value = self.economy.calculate_plant_value(plant)
            self.economy.add_money(value)
            self.garden.remove_plant(x, y)
            self.plants_harvested += 1
            self.total_earnings += value
            
            if plant.is_mutated():
                self.mutations_found += 1
                
            return True
        return False
