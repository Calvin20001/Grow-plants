// Game Class - Main game state management
class Game {
    constructor() {
        this.currentState = STATE_PLAYING;
        this.gameTime = 0.0;
        this.day = 1;
        
        // Core systems
        this.player = new Player();
        this.garden = new Garden();
        this.shop = new Shop();
        this.economy = new Economy();
        
        // Game progression
        this.unlockedPlants = ["carrot"];
        this.unlockedTools = ["basic_watering_can"];
        this.gardenExpansions = 1;
        
        // Weather and events
        this.weather = "sunny";
        this.weatherTimer = 0.0;
        this.activeEvents = [];
        
        // Statistics
        this.plantsHarvested = 0;
        this.totalEarnings = 0;
        this.mutationsFound = 0;
        
        // Input state
        this.keysPressed = new Set();
        this.mousePos = [0, 0];
        this.mouseButtons = { left: false, right: false };
        
        // UI state
        this.showShop = false;
        this.showInventory = false;
        this.showHelp = false;
        
        // Notifications
        this.notifications = [];
        this.notificationTimer = 0.0;
    }
    
    update(dt) {
        this.gameTime += dt;
        this.weatherTimer += dt;
        
        // Update systems
        this.player.update(dt);
        this.garden.update(dt);
        this.economy.update(dt);
        
        // Update weather (every 30 seconds)
        if (this.weatherTimer >= 30.0) {
            this.updateWeather();
            this.weatherTimer = 0.0;
        }
        
        // Check for day change (every 5 minutes)
        if (this.gameTime >= 300.0) {
            this.day++;
            this.gameTime = 0.0;
            this.startNewDay();
        }
        
        // Update notifications
        this.updateNotifications(dt);
    }
    
    updateWeather() {
        const weatherChances = {
            "sunny": 0.6,
            "cloudy": 0.25,
            "rainy": 0.15
        };
        
        const rand = Math.random();
        let cumulative = 0;
        for (const [weather, chance] of Object.entries(weatherChances)) {
            cumulative += chance;
            if (rand <= cumulative) {
                this.weather = weather;
                break;
            }
        }
    }
    
    startNewDay() {
        // Market fluctuations
        this.economy.updateMarketPrices();
        
        // Random events
        this.checkRandomEvents();
    }
    
    checkRandomEvents() {
        // Rainstorm (free watering)
        if (this.weather === "rainy" && Math.random() < 0.3) {
            this.garden.applyRainEffect();
        }
        
        // Market boom (price increase)
        if (Math.random() < 0.1) {
            this.economy.triggerMarketBoom();
        }
        
        // Pest infestation
        if (Math.random() < 0.05) {
            this.garden.triggerPestInfestation();
        }
    }
    
    getPlayerPosition() {
        return [this.player.x, this.player.y];
    }
    
    canAfford(cost) {
        return this.economy.money >= cost;
    }
    
    purchaseItem(itemType, itemName) {
        const item = this.shop.getItem(itemType, itemName);
        if (!item) {
            return false;
        }
        
        if (this.canAfford(item.cost)) {
            this.economy.spendMoney(item.cost);
            
            if (itemType === "seed") {
                this.player.addSeed(itemName);
            } else if (itemType === "tool") {
                this.player.addTool(itemName);
            } else if (itemType === "expansion") {
                this.gardenExpansions++;
                this.garden.expand();
            }
            
            return true;
        }
        return false;
    }
    
    plantSeed(x, y, seedType) {
        if (this.player.hasSeed(seedType)) {
            if (this.garden.plantSeed(x, y, seedType)) {
                this.player.useSeed(seedType);
                return true;
            }
        }
        return false;
    }
    
    waterPlant(x, y) {
        return this.garden.waterPlant(x, y);
    }
    
    harvestPlant(x, y) {
        const plant = this.garden.getPlant(x, y);
        if (plant && plant.isHarvestable()) {
            const value = this.economy.calculatePlantValue(plant);
            this.economy.addMoney(value);
            this.garden.removePlant(x, y);
            this.plantsHarvested++;
            this.totalEarnings += value;
            
            if (plant.isMutated) {
                this.mutationsFound++;
            }
            
            return true;
        }
        return false;
    }
    
    handleKeyDown(key) {
        this.keysPressed.add(key);
        
        switch (key) {
            case 'Escape':
                if (this.showShop || this.showInventory || this.showHelp) {
                    this.showShop = false;
                    this.showInventory = false;
                    this.showHelp = false;
                } else {
                    this.currentState = this.currentState === STATE_PAUSED ? STATE_PLAYING : STATE_PAUSED;
                }
                break;
            case 'e':
            case 'E':
                if (this.currentState !== STATE_PAUSED) {
                    this.showShop = !this.showShop;
                    this.showInventory = false;
                    this.showHelp = false;
                }
                break;
            case 'q':
            case 'Q':
                if (this.currentState !== STATE_PAUSED) {
                    this.showInventory = !this.showInventory;
                    this.showShop = false;
                    this.showHelp = false;
                }
                break;
            case 'h':
            case 'H':
                if (this.currentState !== STATE_PAUSED) {
                    this.showHelp = !this.showHelp;
                    this.showShop = false;
                    this.showInventory = false;
                }
                break;
            case ' ':
                if (this.currentState === STATE_PLAYING && !(this.showShop || this.showInventory || this.showHelp)) {
                    this.handleInteraction();
                }
                break;
        }
    }
    
    handleKeyUp(key) {
        this.keysPressed.delete(key);
    }
    
    handleMouseMove(x, y) {
        this.mousePos = [x, y];
    }
    
    handleMouseDown(button) {
        if (button === 0) { // Left click
            this.mouseButtons.left = true;
        } else if (button === 2) { // Right click
            this.mouseButtons.right = true;
        }
    }
    
    handleMouseUp(button) {
        if (button === 0) {
            this.mouseButtons.left = false;
        } else if (button === 2) {
            this.mouseButtons.right = false;
        }
    }
    
    handleInteraction() {
        const [playerX, playerY] = this.player.getGridPosition();
        
        // Check if player is on a plantable tile
        if (this.garden.isPlantableSoil(playerX, playerY)) {
            const plant = this.garden.getPlant(playerX, playerY);
            
            if (plant === null) {
                // Plant a seed
                const selectedSeed = this.player.getSelectedSeed();
                if (this.plantSeed(playerX, playerY, selectedSeed)) {
                    this.addNotification(`Planted ${selectedSeed}!`);
                } else {
                    this.addNotification("Can't plant here!");
                }
            } else if (plant.isHarvestable()) {
                // Harvest the plant
                if (this.harvestPlant(playerX, playerY)) {
                    const value = plant.getValue();
                    this.addNotification(`Harvested ${plant.name} for ${value} coins!`);
                } else {
                    this.addNotification("Can't harvest this plant!");
                }
            } else {
                // Water or fertilize the plant
                const selectedTool = this.player.getSelectedTool();
                
                if (selectedTool === "basic_watering_can") {
                    if (this.waterPlant(playerX, playerY)) {
                        this.addNotification("Watered the plant!");
                    } else {
                        this.addNotification("Plant doesn't need water!");
                    }
                } else if (selectedTool === "fertilizer_spreader") {
                    if (this.garden.fertilizePlant(playerX, playerY)) {
                        this.addNotification("Applied fertilizer!");
                    } else {
                        this.addNotification("Plant already fertilized!");
                    }
                }
            }
        }
    }
    
    updateNotifications(dt) {
        this.notificationTimer += dt;
        
        // Remove old notifications
        this.notifications = this.notifications.filter(n => n.timer > 0);
        
        // Update remaining notification timers
        for (const notification of this.notifications) {
            notification.timer -= dt;
        }
    }
    
    addNotification(message) {
        this.notifications.push({
            message: message,
            timer: 3.0 // Show for 3 seconds
        });
    }
    
    updatePlayerMovement(dt) {
        // Handle movement based on pressed keys
        this.player.move("left", this.keysPressed.has('a') || this.keysPressed.has('A') || this.keysPressed.has('ArrowLeft'));
        this.player.move("right", this.keysPressed.has('d') || this.keysPressed.has('D') || this.keysPressed.has('ArrowRight'));
        this.player.move("up", this.keysPressed.has('w') || this.keysPressed.has('W') || this.keysPressed.has('ArrowUp'));
        this.player.move("down", this.keysPressed.has('s') || this.keysPressed.has('S') || this.keysPressed.has('ArrowDown'));
    }
}
