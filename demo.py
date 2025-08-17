#!/usr/bin/env python3
"""
Demo script for Grow Plants game
Shows game mechanics without requiring pygame
"""

import sys
import os
import time

# Add the game directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

def demo_plant_growth():
    """Demonstrate plant growth mechanics"""
    print("=== Plant Growth Demo ===\n")
    
    try:
        from plant import Plant
        
        # Create a carrot plant
        plant = Plant("carrot", 5, 5)
        print(f"Planted a {plant.name} at position (5, 5)")
        print(f"Initial stage: {plant.get_current_stage()}")
        print(f"Water need: {plant.water_need}")
        print(f"Base growth time: {plant.base_growth_time} seconds")
        print()
        
        # Simulate growth over time
        print("Simulating plant growth...")
        for i in range(6):
            time.sleep(0.5)  # Simulate time passing
            plant.update(2.0)  # 2 seconds of growth
            
            print(f"Time {i*2}s: Stage = {plant.get_current_stage()}, "
                  f"Progress = {plant.growth_progress:.1f}, "
                  f"Water = {plant.water_level}/{plant.max_water_level}")
            
            # Water the plant every other update
            if i % 2 == 1:
                plant.water()
                print(f"  -> Watered plant!")
        
        print(f"\nFinal plant value: {plant.get_value()} coins")
        print(f"Plant mutated: {plant.is_mutated}")
        if plant.is_mutated:
            print(f"Mutations: {', '.join(plant.mutations)}")
        
    except Exception as e:
        print(f"Demo failed: {e}")

def demo_garden_management():
    """Demonstrate garden management"""
    print("\n=== Garden Management Demo ===\n")
    
    try:
        from garden import Garden
        from plant import Plant
        
        # Create garden
        garden = Garden()
        print(f"Created garden: {garden.width}x{garden.height}")
        print(f"Plantable tiles: {len(garden.get_plantable_positions())}")
        print()
        
        # Plant some seeds
        print("Planting seeds...")
        garden.plant_seed(8, 8, "carrot")
        garden.plant_seed(9, 8, "tomato")
        garden.plant_seed(8, 9, "corn")
        
        print(f"Planted 3 seeds. Total plants: {len(garden.plants)}")
        print()
        
        # Simulate garden updates
        print("Simulating garden updates...")
        for i in range(3):
            time.sleep(0.5)
            garden.update(3.0)  # 3 seconds of growth
            
            print(f"Update {i+1}:")
            for pos, plant in garden.plants.items():
                print(f"  Plant at {pos}: {plant.get_current_stage()}")
        
        # Water plants
        print("\nWatering plants...")
        for pos in garden.plants.keys():
            if garden.water_plant(*pos):
                print(f"  Watered plant at {pos}")
        
        print(f"\nGarden summary: {garden.get_garden_summary()}")
        
    except Exception as e:
        print(f"Demo failed: {e}")

def demo_economy():
    """Demonstrate economy system"""
    print("\n=== Economy Demo ===\n")
    
    try:
        from economy import Economy
        from plant import Plant
        
        # Create economy
        economy = Economy()
        print(f"Starting money: {economy.money} coins")
        print()
        
        # Simulate market changes
        print("Simulating market changes...")
        for i in range(3):
            time.sleep(0.5)
            economy.update_market_prices()
            
            print(f"Day {i+1} prices:")
            for plant_type, price in economy.current_prices.items():
                trend = economy.get_price_trend(plant_type)
                print(f"  {plant_type}: {price} coins ({trend})")
        
        # Test plant value calculation
        print("\nTesting plant value calculation...")
        plant = Plant("carrot", 0, 0)
        
        # Simulate plant growth
        for i in range(4):
            plant.update(2.0)
            value = economy.calculate_plant_value(plant)
            print(f"  Stage {plant.get_current_stage()}: {value} coins")
        
        # Apply fertilizer and water
        plant.fertilize()
        plant.water()
        plant.water()
        
        final_value = economy.calculate_plant_value(plant)
        print(f"  Final value (fertilized + watered): {final_value} coins")
        
        print(f"\nEconomy summary: {economy.get_economic_summary()}")
        
    except Exception as e:
        print(f"Demo failed: {e}")

def demo_shop():
    """Demonstrate shop system"""
    print("\n=== Shop Demo ===\n")
    
    try:
        from shop import Shop
        from economy import Economy
        
        # Create shop and economy
        shop = Shop()
        economy = Economy()
        
        print("Shop inventory:")
        for category in shop.get_all_categories():
            print(f"\n{category.upper()}:")
            items = shop.get_available_items(category)
            for item in items:
                affordable = "✓" if economy.can_afford(item["cost"]) else "✗"
                print(f"  {affordable} {item['name']} - {item['cost']} coins")
                print(f"    {item['description']}")
        
        print(f"\nPlayer money: {economy.money} coins")
        
        # Show recommended items
        recommended = shop.get_recommended_items(economy.money)
        print(f"\nRecommended items (affordable):")
        for item in recommended[:3]:  # Show top 3
            print(f"  {item['name']} - {item['cost']} coins")
        
        print(f"\nShop summary: {shop.get_shop_summary()}")
        
    except Exception as e:
        print(f"Demo failed: {e}")

def demo_player_progression():
    """Demonstrate player progression"""
    print("\n=== Player Progression Demo ===\n")
    
    try:
        from player import Player
        from game_state import GameState
        
        # Create player and game state
        player = Player()
        game_state = GameState()
        
        print(f"Player level: {player.level}")
        print(f"Player experience: {player.experience}/100")
        print(f"Player energy: {player.energy}/{player.max_energy}")
        print()
        
        # Simulate some actions
        print("Simulating player actions...")
        
        # Plant seeds
        for i in range(3):
            if game_state.plant_seed(7+i, 7, "carrot"):
                print(f"  Planted carrot {i+1}")
                player.add_experience(10)
        
        # Water plants
        for i in range(2):
            if game_state.water_plant(7+i, 7):
                print(f"  Watered plant {i+1}")
                player.add_experience(5)
        
        print(f"\nAfter actions:")
        print(f"  Level: {player.level}")
        print(f"  Experience: {player.experience}/100")
        print(f"  Energy: {player.energy}/{player.max_energy}")
        
        print(f"\nInventory: {player.get_inventory_summary()}")
        
    except Exception as e:
        print(f"Demo failed: {e}")

def main():
    """Run all demos"""
    print("🌱 Grow Plants Game Demo 🌱")
    print("=" * 40)
    
    demos = [
        demo_plant_growth,
        demo_garden_management,
        demo_economy,
        demo_shop,
        demo_player_progression
    ]
    
    for demo in demos:
        try:
            demo()
            print("\n" + "="*40 + "\n")
        except Exception as e:
            print(f"Demo failed: {e}")
            print("\n" + "="*40 + "\n")
    
    print("🎉 Demo complete!")
    print("\nTo play the full game, run: python main.py")
    print("To test the game components, run: python test_game.py")

if __name__ == "__main__":
    main()
