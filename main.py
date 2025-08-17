#!/usr/bin/env python3
"""
Grow Plants - Main Game File
A 2D plant-growing simulation game
"""

import pygame
import sys
from game.game_state import GameState
from game.game_loop import GameLoop
from game.constants import *

def main():
    """Main game function"""
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grow Plants")
    clock = pygame.time.Clock()
    
    # Initialize game state
    game_state = GameState()
    
    # Create game loop
    game_loop = GameLoop(screen, game_state, clock)
    
    try:
        # Run the game
        game_loop.run()
    except KeyboardInterrupt:
        print("Game interrupted by user")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
