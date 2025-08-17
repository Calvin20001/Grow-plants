"""
Renderer Class
Handles all game graphics and UI rendering
"""

import pygame
from typing import Dict, List, Optional
from constants import *

class Renderer:
    """Handles all rendering for the game"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        # Initialize fonts
        pygame.font.init()
        self.fonts = {
            16: pygame.font.Font(None, 16),
            18: pygame.font.Font(None, 18),
            20: pygame.font.Font(None, 20),
            24: pygame.font.Font(None, 24),
            32: pygame.font.Font(None, 32),
            48: pygame.font.Font(None, 48)
        }
        
        # Colors for different soil types
        self.soil_colors = {
            0.0: BLACK,      # Unusable
            0.5: LIGHT_BROWN, # Poor soil
            1.0: BROWN,      # Normal soil
            1.5: DARK_GREEN  # Rich soil
        }
    
    def render_garden(self, garden):
        """Render the garden grid"""
        for y in range(garden.height):
            for x in range(garden.width):
                # Calculate screen position
                screen_x = x * GRID_SIZE
                screen_y = y * GRID_SIZE
                
                # Get soil quality
                soil_quality = garden.soil_quality[y][x]
                
                # Determine soil color
                soil_color = self._get_soil_color(soil_quality)
                
                # Draw soil tile
                pygame.draw.rect(
                    self.screen,
                    soil_color,
                    (screen_x, screen_y, GRID_SIZE, GRID_SIZE)
                )
                
                # Draw grid lines
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    (screen_x, screen_y, GRID_SIZE, GRID_SIZE),
                    1
                )
                
                # Draw water level indicator
                if garden.water_levels[y][x] > 0:
                    water_alpha = min(255, garden.water_levels[y][x] * 50)
                    water_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
                    water_surface.set_alpha(water_alpha)
                    water_surface.fill(LIGHT_BLUE)
                    self.screen.blit(water_surface, (screen_x, screen_y))
                
                # Draw fertilizer indicator
                if garden.fertilizer_levels[y][x] > 0:
                    fert_color = GREEN if garden.fertilizer_levels[y][x] >= 2 else LIGHT_GREEN
                    fert_size = min(GRID_SIZE // 4, garden.fertilizer_levels[y][x] * 2)
                    fert_x = screen_x + (GRID_SIZE - fert_size) // 2
                    fert_y = screen_y + (GRID_SIZE - fert_size) // 2
                    pygame.draw.circle(
                        self.screen,
                        fert_color,
                        (fert_x + fert_size // 2, fert_y + fert_size // 2),
                        fert_size // 2
                    )
    
    def render_plant(self, plant):
        """Render a plant"""
        # Get plant visual properties
        props = plant.get_visual_properties()
        
        # Calculate screen position
        screen_x = (plant.x * GRID_SIZE) + (GRID_SIZE // 2)
        screen_y = (plant.y * GRID_SIZE) + (GRID_SIZE // 2)
        
        # Calculate plant size
        plant_size = int(props["size"] * GRID_SIZE * 0.8)
        
        # Draw plant based on stage
        stage = props["stage"]
        color = props["color"]
        
        if stage == "seed":
            # Draw seed
            pygame.draw.circle(
                self.screen,
                BROWN,
                (screen_x, screen_y),
                plant_size // 2
            )
        elif stage == "sprout":
            # Draw sprout
            pygame.draw.circle(
                self.screen,
                LIGHT_GREEN,
                (screen_x, screen_y),
                plant_size // 2
            )
            # Draw stem
            pygame.draw.line(
                self.screen,
                GREEN,
                (screen_x, screen_y),
                (screen_x, screen_y - plant_size // 2),
                2
            )
        elif stage == "small_plant":
            # Draw small plant
            pygame.draw.circle(
                self.screen,
                color,
                (screen_x, screen_y),
                plant_size // 2
            )
            # Draw leaves
            for i in range(3):
                angle = (i * 120) * 3.14159 / 180
                leaf_x = screen_x + int(plant_size * 0.3 * pygame.math.Vector2(1, 0).rotate(angle)[0])
                leaf_y = screen_y + int(plant_size * 0.3 * pygame.math.Vector2(1, 0).rotate(angle)[1])
                pygame.draw.circle(
                    self.screen,
                    GREEN,
                    (leaf_x, leaf_y),
                    plant_size // 4
                )
        elif stage == "mature_plant":
            # Draw mature plant
            pygame.draw.circle(
                self.screen,
                color,
                (screen_x, screen_y),
                plant_size // 2
            )
            # Draw multiple leaves
            for i in range(6):
                angle = (i * 60) * 3.14159 / 180
                leaf_x = screen_x + int(plant_size * 0.4 * pygame.math.Vector2(1, 0).rotate(angle)[0])
                leaf_y = screen_y + int(plant_size * 0.4 * pygame.math.Vector2(1, 0).rotate(angle)[1])
                pygame.draw.circle(
                    self.screen,
                    GREEN,
                    (leaf_x, leaf_y),
                    plant_size // 3
                )
        elif stage == "harvestable":
            # Draw harvestable plant with shine effect
            pygame.draw.circle(
                self.screen,
                color,
                (screen_x, screen_y),
                plant_size // 2
            )
            # Draw shine effect
            shine_size = plant_size // 3
            pygame.draw.circle(
                self.screen,
                WHITE,
                (screen_x - shine_size // 3, screen_y - shine_size // 3),
                shine_size // 2
            )
        
        # Draw mutation indicator
        if props["mutated"]:
            pygame.draw.circle(
                self.screen,
                PURPLE,
                (screen_x, screen_y),
                plant_size // 2 + 2,
                2
            )
        
        # Draw water level indicator
        if props["water_level"] < props["max_water_level"]:
            water_bar_width = GRID_SIZE - 4
            water_bar_height = 4
            water_bar_x = screen_x - water_bar_width // 2
            water_bar_y = screen_y - plant_size // 2 - 8
            
            # Background bar
            pygame.draw.rect(
                self.screen,
                GRAY,
                (water_bar_x, water_bar_y, water_bar_width, water_bar_height)
            )
            
            # Water level
            water_fill = (props["water_level"] / props["max_water_level"]) * water_bar_width
            pygame.draw.rect(
                self.screen,
                BLUE,
                (water_bar_x, water_bar_y, water_fill, water_bar_height)
            )
    
    def render_player(self, player):
        """Render the player character"""
        # Draw player as a simple circle
        pygame.draw.circle(
            self.screen,
            BLUE,
            (int(player.x), int(player.y)),
            PLAYER_SIZE // 2
        )
        
        # Draw player outline
        pygame.draw.circle(
            self.screen,
            WHITE,
            (int(player.x), int(player.y)),
            PLAYER_SIZE // 2,
            2
        )
        
        # Draw direction indicator
        if player.dx != 0 or player.dy != 0:
            # Calculate direction
            direction_x = player.dx * 8
            direction_y = player.dy * 8
            
            pygame.draw.line(
                self.screen,
                WHITE,
                (player.x, player.y),
                (player.x + direction_x, player.y + direction_y),
                3
            )
    
    def render_text(self, text: str, x: int, y: int, color: tuple, size: int, 
                   center: bool = False, alpha: int = 255):
        """Render text on screen"""
        if size not in self.fonts:
            size = 20  # Default size
        
        font = self.fonts[size]
        text_surface = font.render(text, True, color)
        
        if alpha < 255:
            text_surface.set_alpha(alpha)
        
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, (x, y))
    
    def render_shop(self, shop, economy):
        """Render shop interface"""
        # Background
        pygame.draw.rect(
            self.screen,
            DARK_GREEN,
            (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        )
        
        # Title
        self.render_text("SHOP", SCREEN_WIDTH // 2, 130, WHITE, 32, center=True)
        
        # Money display
        money_text = f"Money: {economy.money}"
        self.render_text(money_text, SCREEN_WIDTH // 2, 170, YELLOW, 24, center=True)
        
        # Categories
        categories = shop.get_all_categories()
        y_offset = 220
        
        for category in categories:
            # Category header
            self.render_text(category.upper(), 150, y_offset, WHITE, 20)
            y_offset += 30
            
            # Items in category
            items = shop.get_available_items(category)
            for item in items:
                item_text = f"{item['name']} - {item['cost']} coins"
                self.render_text(item_text, 170, y_offset, LIGHT_GRAY, 18)
                y_offset += 25
            
            y_offset += 20
        
        # Close instruction
        self.render_text("Press ESC to close", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120, WHITE, 18, center=True)
    
    def render_inventory(self, player):
        """Render inventory interface"""
        # Background
        pygame.draw.rect(
            self.screen,
            DARK_GREEN,
            (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        )
        
        # Title
        self.render_text("INVENTORY", SCREEN_WIDTH // 2, 130, WHITE, 32, center=True)
        
        # Player stats
        stats = player.get_inventory_summary()
        y_offset = 180
        
        # Seeds
        self.render_text("SEEDS:", 150, y_offset, WHITE, 20)
        y_offset += 25
        for seed_type, amount in stats["seeds"].items():
            seed_text = f"{seed_type.title()}: {amount}"
            self.render_text(seed_text, 170, y_offset, LIGHT_GRAY, 18)
            y_offset += 20
        
        y_offset += 20
        
        # Tools
        self.render_text("TOOLS:", 150, y_offset, WHITE, 20)
        y_offset += 25
        for tool in stats["tools"]:
            tool_text = f"{tool.replace('_', ' ').title()}"
            color = YELLOW if tool == stats["selected_tool"] else LIGHT_GRAY
            self.render_text(tool_text, 170, y_offset, color, 18)
            y_offset += 20
        
        y_offset += 20
        
        # Stats
        self.render_text(f"Level: {stats['level']}", 150, y_offset, WHITE, 20)
        y_offset += 25
        self.render_text(f"Experience: {stats['experience']}/100", 150, y_offset, WHITE, 20)
        y_offset += 25
        self.render_text(f"Energy: {stats['energy']}/{stats['max_energy']}", 150, y_offset, WHITE, 20)
        
        # Close instruction
        self.render_text("Press ESC to close", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120, WHITE, 18, center=True)
    
    def render_help(self):
        """Render help interface"""
        # Background
        pygame.draw.rect(
            self.screen,
            DARK_GREEN,
            (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        )
        
        # Title
        self.render_text("HELP & CONTROLS", SCREEN_WIDTH // 2, 130, WHITE, 32, center=True)
        
        # Controls
        controls = [
            "WASD or Arrow Keys: Move player",
            "Space: Interact with plants/soil",
            "E: Open shop",
            "Q: Open inventory",
            "H: Show this help",
            "ESC: Pause game or close menus",
            "",
            "GAMEPLAY:",
            "• Plant seeds in soil tiles",
            "• Water plants regularly",
            "• Use fertilizer for better growth",
            "• Harvest mature plants for money",
            "• Buy upgrades in the shop",
            "• Expand your garden area"
        ]
        
        y_offset = 180
        for control in controls:
            if control == "":
                y_offset += 20
                continue
            self.render_text(control, 150, y_offset, LIGHT_GRAY, 18)
            y_offset += 25
        
        # Close instruction
        self.render_text("Press ESC to close", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120, WHITE, 18, center=True)
    
    def render_pause_screen(self):
        """Render pause screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        self.render_text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, WHITE, 48, center=True)
        self.render_text("Press ESC to resume", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE, 24, center=True)
    
    def _get_soil_color(self, quality: float) -> tuple:
        """Get color for soil quality"""
        if quality <= 0.0:
            return self.soil_colors[0.0]
        elif quality <= 0.5:
            return self.soil_colors[0.5]
        elif quality <= 1.0:
            return self.soil_colors[1.0]
        else:
            return self.soil_colors[1.5]
