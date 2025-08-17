"""
Shop Class
Manages available items and their costs
"""

from typing import Dict, List, Optional
from constants import *

class Shop:
    """Shop system for purchasing seeds, tools, and upgrades"""
    
    def __init__(self):
        self.items = {
            "seeds": {
                "carrot": {"name": "Carrot Seeds", "cost": 10, "description": "Fast-growing basic vegetable"},
                "tomato": {"name": "Tomato Seeds", "cost": 25, "description": "Medium growth, good value"},
                "corn": {"name": "Corn Seeds", "cost": 40, "description": "Slow growth, high value"},
                "strawberry": {"name": "Strawberry Seeds", "cost": 60, "description": "Rare fruit, high mutation chance"},
                "sunflower": {"name": "Sunflower Seeds", "cost": 80, "description": "Decorative, attracts beneficial insects"}
            },
            "tools": {
                "basic_watering_can": {"name": "Basic Watering Can", "cost": 0, "description": "Basic watering tool (starter item)"},
                "advanced_watering_can": {"name": "Advanced Watering Can", "cost": 150, "description": "Waters more efficiently"},
                "fertilizer_spreader": {"name": "Fertilizer Spreader", "cost": 200, "description": "Applies fertilizer to multiple plants"},
                "sprinkler": {"name": "Sprinkler System", "cost": 500, "description": "Automatically waters plants"},
                "pest_repellent": {"name": "Pest Repellent", "cost": 300, "description": "Protects plants from pests"}
            },
            "fertilizers": {
                "basic_fertilizer": {"name": "Basic Fertilizer", "cost": 25, "description": "Increases growth rate"},
                "premium_fertilizer": {"name": "Premium Fertilizer", "cost": 75, "description": "Significantly increases growth and mutation chance"},
                "organic_fertilizer": {"name": "Organic Fertilizer", "cost": 100, "description": "Improves soil quality over time"}
            },
            "expansions": {
                "garden_expansion": {"name": "Garden Expansion", "cost": 200, "description": "Unlocks more garden space"},
                "greenhouse": {"name": "Greenhouse", "cost": 1000, "description": "Protects plants from weather, faster growth"}
            }
        }
        
        # Unlock progression
        self.unlocked_categories = ["seeds", "tools"]
        self.unlocked_items = {
            "seeds": ["carrot"],
            "tools": ["basic_watering_can"],
            "fertilizers": [],
            "expansions": []
        }
        
        # Special offers and sales
        self.daily_deals = {}
        self.sale_multiplier = 1.0
    
    def get_item(self, category: str, item_name: str) -> Optional[Dict]:
        """Get item information"""
        if category in self.items and item_name in self.items[category]:
            item = self.items[category][item_name].copy()
            
            # Apply sale multiplier
            if item_name in self.daily_deals:
                item["cost"] = int(item["cost"] * self.daily_deals[item_name])
            else:
                item["cost"] = int(item["cost"] * self.sale_multiplier)
            
            return item
        return None
    
    def get_available_items(self, category: str) -> List[Dict]:
        """Get list of available items in a category"""
        if category not in self.unlocked_categories:
            return []
        
        available = []
        for item_name in self.unlocked_items[category]:
            item = self.get_item(category, item_name)
            if item:
                available.append(item)
        
        return available
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return self.unlocked_categories
    
    def unlock_item(self, category: str, item_name: str) -> bool:
        """Unlock a new item for purchase"""
        if category in self.items and item_name in self.items[category]:
            if category not in self.unlocked_categories:
                self.unlocked_categories.append(category)
            
            if category not in self.unlocked_items:
                self.unlocked_items[category] = []
            
            if item_name not in self.unlocked_items[category]:
                self.unlocked_items[category].append(item_name)
                return True
        
        return False
    
    def unlock_category(self, category: str) -> bool:
        """Unlock an entire category"""
        if category in self.items and category not in self.unlocked_categories:
            self.unlocked_categories.append(category)
            self.unlocked_items[category] = list(self.items[category].keys())
            return True
        return False
    
    def set_sale(self, multiplier: float):
        """Set a general sale multiplier"""
        self.sale_multiplier = max(0.1, min(1.0, multiplier))
    
    def add_daily_deal(self, item_name: str, discount: float):
        """Add a daily deal for a specific item"""
        self.daily_deals[item_name] = max(0.1, min(1.0, 1.0 - discount))
    
    def clear_daily_deals(self):
        """Clear all daily deals"""
        self.daily_deals.clear()
    
    def get_shop_summary(self) -> Dict:
        """Get summary of shop state"""
        return {
            "unlocked_categories": self.unlocked_categories.copy(),
            "unlocked_items": {cat: items.copy() for cat, items in self.unlocked_items.items()},
            "sale_multiplier": self.sale_multiplier,
            "daily_deals": self.daily_deals.copy()
        }
    
    def can_afford_item(self, category: str, item_name: str, money: int) -> bool:
        """Check if player can afford an item"""
        item = self.get_item(category, item_name)
        if not item:
            return False
        return money >= item["cost"]
    
    def get_item_cost(self, category: str, item_name: str) -> int:
        """Get the cost of an item"""
        item = self.get_item(category, item_name)
        return item["cost"] if item else 0
    
    def get_recommended_items(self, money: int, category: str = None) -> List[Dict]:
        """Get items the player can afford, optionally filtered by category"""
        recommended = []
        
        categories = [category] if category else self.unlocked_categories
        
        for cat in categories:
            if cat not in self.unlocked_categories:
                continue
                
            for item_name in self.unlocked_items[cat]:
                if self.can_afford_item(cat, item_name, money):
                    item = self.get_item(cat, item_name)
                    if item:
                        recommended.append(item)
        
        # Sort by cost (cheapest first)
        recommended.sort(key=lambda x: x["cost"])
        return recommended
