"""
Game Constants and Configuration
"""

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Game grid
GRID_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Player settings
PLAYER_SPEED = 3
PLAYER_SIZE = 24

# Plant growth settings
BASE_GROWTH_TIME = 10.0  # seconds
WATERING_BONUS = 0.5
FERTILIZER_BONUS = 0.3
MUTATION_CHANCE = 0.05
RARE_MUTATION_CHANCE = 0.02

# Economy
STARTING_MONEY = 100
BASIC_SEED_COST = 10
FERTILIZER_COST = 25
BASIC_PLANT_VALUE = 20

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_SHOP = "shop"
STATE_INVENTORY = "inventory"
STATE_PAUSED = "paused"

# Plant types
PLANT_TYPES = {
    "carrot": {
        "name": "Carrot",
        "growth_time": 8.0,
        "water_need": 2,
        "base_value": 15,
        "mutation_chance": 0.08,
        "color": ORANGE
    },
    "tomato": {
        "name": "Tomato",
        "growth_time": 12.0,
        "water_need": 3,
        "base_value": 25,
        "mutation_chance": 0.06,
        "color": RED
    },
    "corn": {
        "name": "Corn",
        "growth_time": 15.0,
        "water_need": 4,
        "base_value": 35,
        "mutation_chance": 0.04,
        "color": YELLOW
    }
}

# Growth stages
GROWTH_STAGES = [
    "seed",
    "sprout", 
    "small_plant",
    "mature_plant",
    "harvestable"
]
