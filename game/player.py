"""
Player Class
Handles player movement, inventory, and interactions
"""

from typing import Dict, List
from constants import *

class Player:
    """Player character with movement and inventory"""
    
    def __init__(self):
        # Position (center of screen initially)
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        
        # Movement
        self.speed = PLAYER_SPEED
        self.dx = 0
        self.dy = 0
        
        # Inventory
        self.seeds = {"carrot": 5}  # Start with some carrot seeds
        self.tools = ["basic_watering_can"]
        self.selected_tool = "basic_watering_can"
        self.selected_seed = "carrot"
        
        # Stats
        self.energy = 100
        self.max_energy = 100
        self.experience = 0
        self.level = 1
        
    def update(self, dt: float):
        """Update player state"""
        # Update position based on movement
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        
        # Keep player on screen
        self.x = max(PLAYER_SIZE // 2, min(SCREEN_WIDTH - PLAYER_SIZE // 2, self.x))
        self.y = max(PLAYER_SIZE // 2, min(SCREEN_HEIGHT - PLAYER_SIZE // 2, self.y))
        
        # Regenerate energy slowly
        if self.energy < self.max_energy:
            self.energy += 10 * dt  # 10 energy per second
    
    def move(self, direction: str, pressed: bool):
        """Handle movement input"""
        if direction == "left":
            self.dx = -1 if pressed else 0
        elif direction == "right":
            self.dx = 1 if pressed else 0
        elif direction == "up":
            self.dy = -1 if pressed else 0
        elif direction == "down":
            self.dy = 1 if pressed else 0
    
    def get_grid_position(self) -> tuple:
        """Get player position in grid coordinates"""
        grid_x = int(self.x // GRID_SIZE)
        grid_y = int(self.y // GRID_SIZE)
        return grid_x, grid_y
    
    def get_world_position(self) -> tuple:
        """Get player position in world coordinates"""
        return self.x, self.y
    
    def add_seed(self, seed_type: str, amount: int = 1):
        """Add seeds to inventory"""
        if seed_type in self.seeds:
            self.seeds[seed_type] += amount
        else:
            self.seeds[seed_type] = amount
    
    def use_seed(self, seed_type: str) -> bool:
        """Use a seed from inventory"""
        if self.has_seed(seed_type):
            self.seeds[seed_type] -= 1
            if self.seeds[seed_type] <= 0:
                del self.seeds[seed_type]
            return True
        return False
    
    def has_seed(self, seed_type: str) -> bool:
        """Check if player has a specific seed"""
        return seed_type in self.seeds and self.seeds[seed_type] > 0
    
    def add_tool(self, tool_name: str):
        """Add a tool to inventory"""
        if tool_name not in self.tools:
            self.tools.append(tool_name)
    
    def select_tool(self, tool_name: str):
        """Select a tool to use"""
        if tool_name in self.tools:
            self.selected_tool = tool_name
    
    def select_seed(self, seed_type: str):
        """Select a seed type to plant"""
        if self.has_seed(seed_type):
            self.selected_seed = seed_type
    
    def get_selected_seed(self) -> str:
        """Get currently selected seed type"""
        return self.selected_seed
    
    def get_selected_tool(self) -> str:
        """Get currently selected tool"""
        return self.selected_tool
    
    def use_energy(self, amount: int) -> bool:
        """Use energy for actions"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def add_experience(self, amount: int):
        """Add experience points"""
        self.experience += amount
        
        # Level up every 100 experience
        while self.experience >= 100:
            self.experience -= 100
            self.level += 1
            self.max_energy += 10
            self.energy = self.max_energy
    
    def get_inventory_summary(self) -> Dict:
        """Get summary of player inventory"""
        return {
            "seeds": self.seeds.copy(),
            "tools": self.tools.copy(),
            "selected_tool": self.selected_tool,
            "selected_seed": self.selected_seed,
            "energy": self.energy,
            "max_energy": self.max_energy,
            "level": self.level,
            "experience": self.experience
        }
