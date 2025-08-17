"""
Input Handler Class
Manages user input and input state
"""

from typing import Dict, Set
import pygame

class InputHandler:
    """Handles and tracks user input state"""
    
    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {1: False, 2: False, 3: False}  # Left, Middle, Right
        self.mouse_buttons_just_pressed = {1: False, 2: False, 3: False}
        self.mouse_buttons_just_released = {1: False, 2: False, 3: False}
    
    def update(self):
        """Update input state - call this at the start of each frame"""
        # Clear just pressed/released states
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        
        for button in self.mouse_buttons_just_pressed:
            self.mouse_buttons_just_pressed[button] = False
            self.mouse_buttons_just_released[button] = False
        
        # Update mouse position
        self.mouse_pos = pygame.mouse.get_pos()
    
    def handle_event(self, event):
        """Handle a pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key not in self.keys_pressed:
                self.keys_pressed.add(event.key)
                self.keys_just_pressed.add(event.key)
        
        elif event.type == pygame.KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed.remove(event.key)
                self.keys_just_released.add(event.key)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button = event.button
            if button in self.mouse_buttons:
                self.mouse_buttons[button] = True
                self.mouse_buttons_just_pressed[button] = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            button = event.button
            if button in self.mouse_buttons:
                self.mouse_buttons[button] = False
                self.mouse_buttons_just_released[button] = True
    
    def is_key_pressed(self, key) -> bool:
        """Check if a key is currently pressed"""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key) -> bool:
        """Check if a key was just pressed this frame"""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key) -> bool:
        """Check if a key was just released this frame"""
        return key in self.keys_just_released
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if a mouse button is currently pressed"""
        return self.mouse_buttons.get(button, False)
    
    def is_mouse_button_just_pressed(self, button: int) -> bool:
        """Check if a mouse button was just pressed this frame"""
        return self.mouse_buttons_just_pressed.get(button, False)
    
    def is_mouse_button_just_released(self, button: int) -> bool:
        """Check if a mouse button was just released this frame"""
        return self.mouse_buttons_just_released.get(button, False)
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position"""
        return self.mouse_pos
    
    def get_mouse_grid_position(self, grid_size: int) -> tuple:
        """Get mouse position in grid coordinates"""
        x, y = self.mouse_pos
        return x // grid_size, y // grid_size
    
    def get_pressed_keys(self) -> Set:
        """Get all currently pressed keys"""
        return self.keys_pressed.copy()
    
    def get_just_pressed_keys(self) -> Set:
        """Get all keys pressed this frame"""
        return self.keys_just_pressed.copy()
    
    def get_just_released_keys(self) -> Set:
        """Get all keys released this frame"""
        return self.keys_just_released.copy()
    
    def clear_input_state(self):
        """Clear all input state (useful for resetting)"""
        self.keys_pressed.clear()
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        
        for button in self.mouse_buttons:
            self.mouse_buttons[button] = False
            self.mouse_buttons_just_pressed[button] = False
            self.mouse_buttons_just_released[button] = False
