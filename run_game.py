#!/usr/bin/env python3
"""
Game Launcher for Grow Plants
Checks dependencies and launches the game
"""

import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} found")
    except ImportError:
        print("✗ Pygame not found. Installing...")
        os.system("pip install pygame")
        try:
            import pygame
            print(f"✓ Pygame {pygame.version.ver} installed successfully")
        except ImportError:
            print("✗ Failed to install pygame. Please install manually:")
            print("  pip install pygame")
            return False
    
    try:
        import numpy
        print(f"✓ NumPy {numpy.__version__} found")
    except ImportError:
        print("✗ NumPy not found. Installing...")
        os.system("pip install numpy")
        try:
            import numpy
            print(f"✓ NumPy {numpy.__version__} installed successfully")
        except ImportError:
            print("✗ Failed to install numpy. Please install manually:")
            print("  pip install numpy")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("🌱 Grow Plants Game Launcher 🌱")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies not met. Cannot launch game.")
        return
    
    print("\n✓ All dependencies satisfied!")
    
    # Try to launch the game
    try:
        print("\n🚀 Launching Grow Plants...")
        print("Controls:")
        print("  WASD/Arrow Keys: Move")
        print("  Space: Interact")
        print("  E: Shop")
        print("  Q: Inventory")
        print("  H: Help")
        print("  ESC: Pause/Close")
        print("\nPress Ctrl+C to exit")
        
        # Import and run the game
        from game.game_state import GameState
        from game.game_loop import GameLoop
        from game.constants import *
        
        import pygame
        pygame.init()
        
        # Set up display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Grow Plants")
        clock = pygame.time.Clock()
        
        # Initialize game state
        game_state = GameState()
        
        # Create game loop
        game_loop = GameLoop(screen, game_state, clock)
        
        # Run the game
        game_loop.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted by user")
    except Exception as e:
        print(f"\n❌ Error launching game: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed")
        print("2. Check that all game files are present")
        print("3. Try running: python test_game.py")
    finally:
        try:
            pygame.quit()
        except:
            pass

if __name__ == "__main__":
    main()
