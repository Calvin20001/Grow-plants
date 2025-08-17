"""
Economy Class
Manages money, market prices, and economic systems
"""

import random
import time
from typing import Dict, List
from constants import *
from plant import Plant

class Economy:
    """Economic system for the game"""
    
    def __init__(self):
        self.money = STARTING_MONEY
        self.total_earned = 0
        self.total_spent = 0
        
        # Market prices and fluctuations
        self.base_prices = {
            "carrot": 15,
            "tomato": 25,
            "corn": 35,
            "strawberry": 50,
            "sunflower": 40
        }
        
        self.current_prices = self.base_prices.copy()
        self.price_multipliers = {plant: 1.0 for plant in self.base_prices}
        
        # Market events
        self.market_boom = False
        self.market_boom_timer = 0.0
        self.market_crash = False
        self.market_crash_timer = 0.0
        
        # Price history for trends
        self.price_history = {plant: [] for plant in self.base_prices}
        self.max_history_length = 10
        
        # Economic milestones
        self.milestones = {
            100: "First Harvest",
            500: "Small Farmer",
            1000: "Established Gardener",
            2500: "Plant Master",
            5000: "Garden Empire",
            10000: "Plant Legend"
        }
        self.achieved_milestones = set()
    
    def update(self, dt: float):
        """Update economy state"""
        # Update market events
        if self.market_boom:
            self.market_boom_timer -= dt
            if self.market_boom_timer <= 0:
                self._end_market_boom()
        
        if self.market_crash:
            self.market_crash_timer -= dt
            if self.market_crash_timer <= 0:
                self._end_market_crash()
        
        # Check milestones
        self._check_milestones()
    
    def add_money(self, amount: int):
        """Add money to player's balance"""
        self.money += amount
        self.total_earned += amount
    
    def spend_money(self, amount: int) -> bool:
        """Spend money from player's balance"""
        if self.money >= amount:
            self.money -= amount
            self.total_spent += amount
            return True
        return False
    
    def can_afford(self, cost: int) -> bool:
        """Check if player can afford a cost"""
        return self.money >= cost
    
    def get_balance(self) -> int:
        """Get current money balance"""
        return self.money
    
    def calculate_plant_value(self, plant: Plant) -> int:
        """Calculate the value of a harvested plant"""
        base_value = self.current_prices.get(plant.plant_type, 20)
        
        # Apply plant-specific modifiers
        value = base_value
        
        # Stage bonus (more mature plants worth more)
        stage_bonus = 1.0 + (plant.current_stage * 0.1)
        value *= stage_bonus
        
        # Mutation bonus
        if plant.is_mutated:
            value *= 2.0  # Mutated plants worth double
        
        # Care bonus
        care_bonus = 1.0
        if plant.fertilized:
            care_bonus += 0.2
        if plant.water_level >= plant.max_water_level:
            care_bonus += 0.1
        
        value *= care_bonus
        
        # Market condition bonus
        if self.market_boom:
            value = int(value * 1.5)
        elif self.market_crash:
            value = int(value * 0.7)
        
        return max(1, int(value))
    
    def update_market_prices(self):
        """Update market prices (called daily)"""
        for plant_type in self.base_prices:
            # Random price fluctuation
            fluctuation = random.uniform(-0.1, 0.1)
            self.price_multipliers[plant_type] += fluctuation
            
            # Keep multipliers within reasonable bounds
            self.price_multipliers[plant_type] = max(0.5, min(2.0, self.price_multipliers[plant_type]))
            
            # Update current price
            self.current_prices[plant_type] = int(self.base_prices[plant_type] * self.price_multipliers[plant_type])
            
            # Add to price history
            self.price_history[plant_type].append(self.current_prices[plant_type])
            if len(self.price_history[plant_type]) > self.max_history_length:
                self.price_history[plant_type].pop(0)
    
    def trigger_market_boom(self):
        """Trigger a market boom event"""
        if not self.market_boom:
            self.market_boom = True
            self.market_boom_timer = 60.0  # Boom lasts 1 minute
            
            # Increase all prices
            for plant_type in self.current_prices:
                self.current_prices[plant_type] = int(self.current_prices[plant_type] * 1.5)
    
    def trigger_market_crash(self):
        """Trigger a market crash event"""
        if not self.market_crash:
            self.market_crash = True
            self.market_crash_timer = 45.0  # Crash lasts 45 seconds
            
            # Decrease all prices
            for plant_type in self.current_prices:
                self.current_prices[plant_type] = int(self.current_prices[plant_type] * 0.7)
    
    def _end_market_boom(self):
        """End market boom event"""
        self.market_boom = False
        self.market_boom_timer = 0.0
        
        # Reset prices to normal
        for plant_type in self.current_prices:
            self.current_prices[plant_type] = int(self.base_prices[plant_type] * self.price_multipliers[plant_type])
    
    def _end_market_crash(self):
        """End market crash event"""
        self.market_crash = False
        self.market_crash_timer = 0.0
        
        # Reset prices to normal
        for plant_type in self.current_prices:
            self.current_prices[plant_type] = int(self.base_prices[plant_type] * self.price_multipliers[plant_type])
    
    def _check_milestones(self):
        """Check for economic milestones"""
        for milestone_amount in sorted(self.milestones.keys()):
            if (self.total_earned >= milestone_amount and 
                milestone_amount not in self.achieved_milestones):
                self.achieved_milestones.add(milestone_amount)
                # Could trigger achievement notification here
    
    def get_market_summary(self) -> Dict:
        """Get summary of market conditions"""
        return {
            "current_prices": self.current_prices.copy(),
            "base_prices": self.base_prices.copy(),
            "price_multipliers": self.price_multipliers.copy(),
            "market_boom": self.market_boom,
            "market_crash": self.market_crash,
            "boom_timer": self.market_boom_timer,
            "crash_timer": self.market_crash_timer
        }
    
    def get_economic_summary(self) -> Dict:
        """Get summary of economic state"""
        return {
            "money": self.money,
            "total_earned": self.total_earned,
            "total_spent": self.total_spent,
            "net_worth": self.money,
            "achieved_milestones": list(self.achieved_milestones),
            "next_milestone": self._get_next_milestone()
        }
    
    def _get_next_milestone(self) -> str:
        """Get the next milestone to achieve"""
        for milestone_amount in sorted(self.milestones.keys()):
            if milestone_amount > self.total_earned:
                return f"{self.milestones[milestone_amount]} ({milestone_amount - self.total_earned} more needed)"
        return "All milestones achieved!"
    
    def get_price_trend(self, plant_type: str) -> str:
        """Get price trend for a plant type"""
        if plant_type not in self.price_history or len(self.price_history[plant_type]) < 2:
            return "stable"
        
        history = self.price_history[plant_type]
        if len(history) >= 2:
            recent_change = history[-1] - history[-2]
            if recent_change > 0:
                return "rising"
            elif recent_change < 0:
                return "falling"
        
        return "stable"
    
    def get_best_investment(self) -> str:
        """Get recommendation for best plant to invest in"""
        best_plant = None
        best_ratio = 0
        
        for plant_type, current_price in self.current_prices.items():
            base_price = self.base_prices[plant_type]
            ratio = current_price / base_price
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_plant = plant_type
        
        return best_plant if best_plant else "carrot"
