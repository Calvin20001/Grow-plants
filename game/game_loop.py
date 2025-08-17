"""
Game Loop
Main game loop handling input, updates, and rendering
"""

import pygame
from typing import Dict, List
from constants import *
from renderer import Renderer
from input_handler import InputHandler

class GameLoop:
    """Main game loop for the plant-growing game"""
    
    def __init__(self, screen: pygame.Surface, game_state, clock: pygame.time.Clock):
        self.screen = screen
        self.game_state = game_state
        self.clock = clock
        
        # Systems
        self.renderer = Renderer(screen)
        self.input_handler = InputHandler()
        
        # Game state
        self.running = True
        self.paused = False
        
        # Performance
        self.fps = 60
        self.last_time = pygame.time.get_ticks()
        
        # UI state
        self.show_shop = False
        self.show_inventory = False
        self.show_help = False
        
        # Notifications
        self.notifications = []
        self.notification_timer = 0.0
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self._handle_events()
            
            # Update game state
            if not self.paused:
                self._update()
            
            # Render everything
            self._render()
            
            # Cap frame rate
            self.clock.tick(self.fps)
    
    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos, event.button)
    
    def _handle_keydown(self, key):
        """Handle key press events"""
        if key == pygame.K_ESCAPE:
            if self.show_shop or self.show_inventory or self.show_help:
                self.show_shop = False
                self.show_inventory = False
                self.show_help = False
            else:
                self.paused = not self.paused
        
        elif key == pygame.K_e:
            if not self.paused:
                self.show_shop = not self.show_shop
                self.show_inventory = False
                self.show_help = False
        
        elif key == pygame.K_q:
            if not self.paused:
                self.show_inventory = not self.show_inventory
                self.show_shop = False
                self.show_help = False
        
        elif key == pygame.K_h:
            if not self.paused:
                self.show_help = not self.show_help
                self.show_shop = False
                self.show_inventory = False
        
        elif key == pygame.K_SPACE:
            if not self.paused and not (self.show_shop or self.show_inventory or self.show_help):
                self._handle_interaction()
        
        # Movement keys
        elif key in [pygame.K_w, pygame.K_UP]:
            self.game_state.player.move("up", True)
        elif key in [pygame.K_s, pygame.K_DOWN]:
            self.game_state.player.move("down", True)
        elif key in [pygame.K_a, pygame.K_LEFT]:
            self.game_state.player.move("left", True)
        elif key in [pygame.K_d, pygame.K_RIGHT]:
            self.game_state.player.move("right", True)
    
    def _handle_keyup(self, key):
        """Handle key release events"""
        # Movement keys
        if key in [pygame.K_w, pygame.K_UP]:
            self.game_state.player.move("up", False)
        elif key in [pygame.K_s, pygame.K_DOWN]:
            self.game_state.player.move("down", False)
        elif key in [pygame.K_a, pygame.K_LEFT]:
            self.game_state.player.move("left", False)
        elif key in [pygame.K_d, pygame.K_RIGHT]:
            self.game_state.player.move("right", False)
    
    def _handle_mouse_click(self, pos, button):
        """Handle mouse click events"""
        if button == 1:  # Left click
            if self.show_shop:
                self._handle_shop_click(pos)
            elif self.show_inventory:
                self._handle_inventory_click(pos)
            else:
                self._handle_garden_click(pos)
    
    def _handle_interaction(self):
        """Handle space bar interaction"""
        player_x, player_y = self.game_state.player.get_grid_position()
        
        # Check if player is on a plantable tile
        if self.game_state.garden._is_plantable_soil(player_x, player_y):
            plant = self.game_state.garden.get_plant(player_x, player_y)
            
            if plant is None:
                # Plant a seed
                selected_seed = self.game_state.player.get_selected_seed()
                if self.game_state.plant_seed(player_x, player_y, selected_seed):
                    self._add_notification(f"Planted {selected_seed}!")
                else:
                    self._add_notification("Can't plant here!")
            
            elif plant.is_harvestable():
                # Harvest the plant
                if self.game_state.harvest_plant(player_x, player_y):
                    value = plant.get_value()
                    self._add_notification(f"Harvested {plant.name} for {value} coins!")
                else:
                    self._add_notification("Can't harvest this plant!")
            
            else:
                # Water or fertilize the plant
                selected_tool = self.game_state.player.get_selected_tool()
                
                if selected_tool == "basic_watering_can":
                    if self.game_state.water_plant(player_x, player_y):
                        self._add_notification("Watered the plant!")
                    else:
                        self._add_notification("Plant doesn't need water!")
                
                elif selected_tool == "fertilizer_spreader":
                    if self.game_state.garden.fertilize_plant(player_x, player_y):
                        self._add_notification("Applied fertilizer!")
                    else:
                        self._add_notification("Plant already fertilized!")
    
    def _handle_shop_click(self, pos):
        """Handle clicks in the shop interface"""
        # This would handle shop item selection and purchase
        # For now, just close the shop
        self.show_shop = False
    
    def _handle_inventory_click(self, pos):
        """Handle clicks in the inventory interface"""
        # This would handle inventory item selection
        # For now, just close the inventory
        self.show_inventory = False
    
    def _handle_garden_click(self, pos):
        """Handle clicks in the garden area"""
        # Convert screen position to grid position
        grid_x = pos[0] // GRID_SIZE
        grid_y = pos[1] // GRID_SIZE
        
        # Check if it's a valid garden position
        if (0 <= grid_x < self.game_state.garden.width and 
            0 <= grid_y < self.game_state.garden.height):
            
            # Move player to clicked position
            self.game_state.player.x = (grid_x * GRID_SIZE) + (GRID_SIZE // 2)
            self.game_state.player.y = (grid_y * GRID_SIZE) + (GRID_SIZE // 2)
    
    def _update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_time) / 1000.0  # Convert to seconds
        self.last_time = current_time
        
        # Update game state
        self.game_state.update(dt)
        
        # Update notifications
        self._update_notifications(dt)
    
    def _update_notifications(self, dt):
        """Update notification system"""
        self.notification_timer += dt
        
        # Remove old notifications
        self.notifications = [n for n in self.notifications if n["timer"] > 0]
        
        # Update remaining notification timers
        for notification in self.notifications:
            notification["timer"] -= dt
    
    def _add_notification(self, message: str):
        """Add a new notification"""
        self.notifications.append({
            "message": message,
            "timer": 3.0  # Show for 3 seconds
        })
    
    def _render(self):
        """Render the game"""
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.paused:
            self._render_pause_screen()
        elif self.show_shop:
            self._render_shop()
        elif self.show_inventory:
            self._render_inventory()
        elif self.show_help:
            self._render_help()
        else:
            self._render_game()
        
        # Render notifications
        self._render_notifications()
        
        # Update display
        pygame.display.flip()
    
    def _render_game(self):
        """Render the main game view"""
        # Render garden
        self.renderer.render_garden(self.game_state.garden)
        
        # Render plants
        for plant in self.game_state.garden.plants.values():
            self.renderer.render_plant(plant)
        
        # Render player
        self.renderer.render_player(self.game_state.player)
        
        # Render UI
        self._render_game_ui()
    
    def _render_game_ui(self):
        """Render in-game UI elements"""
        # Money display
        money_text = f"Money: {self.game_state.economy.money}"
        self.renderer.render_text(money_text, 10, 10, WHITE, 24)
        
        # Day display
        day_text = f"Day: {self.game_state.day}"
        self.renderer.render_text(day_text, 10, 40, WHITE, 20)
        
        # Weather display
        weather_text = f"Weather: {self.game_state.weather.title()}"
        self.renderer.render_text(weather_text, 10, 70, WHITE, 20)
        
        # Selected seed/tool
        seed_text = f"Seed: {self.game_state.player.get_selected_seed()}"
        self.renderer.render_text(seed_text, 10, 100, WHITE, 18)
        
        tool_text = f"Tool: {self.game_state.player.get_selected_tool()}"
        self.renderer.render_text(tool_text, 10, 125, WHITE, 18)
        
        # Controls help
        controls = [
            "WASD: Move",
            "Space: Interact",
            "E: Shop",
            "Q: Inventory",
            "H: Help",
            "ESC: Pause"
        ]
        
        for i, control in enumerate(controls):
            self.renderer.render_text(control, SCREEN_WIDTH - 200, 10 + (i * 20), LIGHT_GRAY, 16)
    
    def _render_shop(self):
        """Render shop interface"""
        self.renderer.render_shop(self.game_state.shop, self.game_state.economy)
    
    def _render_inventory(self):
        """Render inventory interface"""
        self.renderer.render_inventory(self.game_state.player)
    
    def _render_help(self):
        """Render help interface"""
        self.renderer.render_help()
    
    def _render_pause_screen(self):
        """Render pause screen"""
        self.renderer.render_pause_screen()
    
    def _render_notifications(self):
        """Render notification messages"""
        y_offset = 200
        for notification in self.notifications:
            if notification["timer"] > 0:
                alpha = min(255, int(255 * (notification["timer"] / 3.0)))
                self.renderer.render_text(
                    notification["message"],
                    SCREEN_WIDTH // 2,
                    y_offset,
                    WHITE,
                    20,
                    center=True,
                    alpha=alpha
                )
                y_offset += 30
