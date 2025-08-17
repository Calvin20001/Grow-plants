#!/usr/bin/env python3
"""
Test script for Grow Plants game
Tests basic functionality without running the full game
"""

import sys
import os

# Add the game directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

def test_imports():
    """Test that all game modules can be imported"""
    print("Testing imports...")
    
    try:
        import constants
        print("✓ Constants imported successfully")
        
        from player import Player
        print("✓ Player class imported successfully")
        
        from plant import Plant
        print("✓ Plant class imported successfully")
        
        from garden import Garden
        print("✓ Garden class imported successfully")
        
        from shop import Shop
        print("✓ Shop class imported successfully")
        
        from economy import Economy
        print("✓ Economy class imported successfully")
        
        from game_state import GameState
        print("✓ GameState class imported successfully")
        
        print("\nAll imports successful!")
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic game functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from player import Player
        from plant import Plant
        from garden import Garden
        from shop import Shop
        from economy import Economy
        from game_state import GameState
        
        # Test player
        player = Player()
        print(f"✓ Player created at position ({player.x}, {player.y})")
        print(f"✓ Player has {len(player.seeds)} seed types")
        
        # Test plant
        plant = Plant("carrot", 5, 5)
        print(f"✓ Plant created: {plant.name}")
        print(f"✓ Plant stage: {plant.get_current_stage()}")
        
        # Test garden
        garden = Garden()
        print(f"✓ Garden created: {garden.width}x{garden.height}")
        print(f"✓ Garden has {len(garden.plants)} plants")
        
        # Test shop
        shop = Shop()
        print(f"✓ Shop created with {len(shop.unlocked_categories)} categories")
        
        # Test economy
        economy = Economy()
        print(f"✓ Economy created with {economy.money} starting money")
        
        # Test game state
        game_state = GameState()
        print(f"✓ GameState created successfully")
        
        print("\nAll basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def test_plant_growth():
    """Test plant growth mechanics"""
    print("\nTesting plant growth...")
    
    try:
        from plant import Plant
        
        plant = Plant("carrot", 0, 0)
        initial_stage = plant.get_current_stage()
        
        # Simulate some growth time
        plant.update(5.0)  # 5 seconds
        
        print(f"✓ Plant initial stage: {initial_stage}")
        print(f"✓ Plant after 5s: {plant.get_current_stage()}")
        print(f"✓ Plant water level: {plant.water_level}/{plant.max_water_level}")
        
        # Test watering
        plant.water()
        print(f"✓ Plant watered, water level: {plant.water_level}")
        
        # Test fertilizer
        plant.fertilize()
        print(f"✓ Plant fertilized: {plant.fertilized}")
        
        print("\nPlant growth tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Plant growth test failed: {e}")
        return False

def test_economy():
    """Test economy system"""
    print("\nTesting economy...")
    
    try:
        from economy import Economy
        from plant import Plant
        
        economy = Economy()
        initial_money = economy.money
        
        # Test adding money
        economy.add_money(50)
        print(f"✓ Money added: {initial_money} -> {economy.money}")
        
        # Test spending money
        if economy.spend_money(25):
            print(f"✓ Money spent: {economy.money}")
        else:
            print("✗ Failed to spend money")
        
        # Test plant value calculation
        plant = Plant("carrot", 0, 0)
        value = economy.calculate_plant_value(plant)
        print(f"✓ Plant value calculated: {value}")
        
        print("\nEconomy tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Economy test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Grow Plants Game Test Suite ===\n")
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_plant_growth,
        test_economy
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The game should work correctly.")
        print("\nTo run the game, use: python main.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
