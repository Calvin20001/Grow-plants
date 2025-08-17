// Game Constants and Configuration
const SCREEN_WIDTH = 1024;
const SCREEN_HEIGHT = 768;

// Game grid
const GRID_SIZE = 32;
const GRID_WIDTH = 20;
const GRID_HEIGHT = 15;

// Colors
const COLORS = {
    BLACK: '#000000',
    WHITE: '#FFFFFF',
    GREEN: '#228B22',
    BROWN: '#8B4513',
    LIGHT_BROWN: '#A0522D',
    BLUE: '#0000FF',
    LIGHT_BLUE: '#ADD8E6',
    GRAY: '#808080',
    LIGHT_GRAY: '#C0C0C0',
    DARK_GREEN: '#006400',
    YELLOW: '#FFFF00',
    RED: '#FF0000',
    PURPLE: '#800080',
    ORANGE: '#FFA500',
    LIGHT_GREEN: '#90EE90'
};

// Player settings
const PLAYER_SPEED = 3;
const PLAYER_SIZE = 24;

// Plant growth settings
const BASE_GROWTH_TIME = 10.0; // seconds
const WATERING_BONUS = 0.5;
const FERTILIZER_BONUS = 0.3;
const MUTATION_CHANCE = 0.05;
const RARE_MUTATION_CHANCE = 0.02;

// Economy
const STARTING_MONEY = 100;
const BASIC_SEED_COST = 10;
const FERTILIZER_COST = 25;
const BASIC_PLANT_VALUE = 20;

// Game states
const STATE_MENU = "menu";
const STATE_PLAYING = "playing";
const STATE_SHOP = "shop";
const STATE_INVENTORY = "inventory";
const STATE_PAUSED = "paused";

// Plant types
const PLANT_TYPES = {
    "carrot": {
        name: "Carrot",
        growth_time: 8.0,
        water_need: 2,
        base_value: 15,
        mutation_chance: 0.08,
        color: COLORS.ORANGE
    },
    "tomato": {
        name: "Tomato",
        growth_time: 12.0,
        water_need: 3,
        base_value: 25,
        mutation_chance: 0.06,
        color: COLORS.RED
    },
    "corn": {
        name: "Corn",
        growth_time: 15.0,
        water_need: 4,
        base_value: 35,
        mutation_chance: 0.04,
        color: COLORS.YELLOW
    }
};

// Growth stages
const GROWTH_STAGES = [
    "seed",
    "sprout", 
    "small_plant",
    "mature_plant",
    "harvestable"
];
