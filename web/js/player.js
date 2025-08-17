// Player Class - Handles player movement, inventory, and interactions
class Player {
    constructor() {
        // Position (center of screen initially)
        this.x = SCREEN_WIDTH / 2;
        this.y = SCREEN_HEIGHT / 2;
        
        // Movement
        this.speed = PLAYER_SPEED;
        this.dx = 0;
        this.dy = 0;
        
        // Inventory
        this.seeds = { "carrot": 5 }; // Start with some carrot seeds
        this.tools = ["basic_watering_can"];
        this.selectedTool = "basic_watering_can";
        this.selectedSeed = "carrot";
        
        // Stats
        this.energy = 100;
        this.maxEnergy = 100;
        this.experience = 0;
        this.level = 1;
    }
    
    update(dt) {
        // Update position based on movement
        this.x += this.dx * this.speed * dt;
        this.y += this.dy * this.speed * dt;
        
        // Keep player on screen
        this.x = Math.max(PLAYER_SIZE / 2, Math.min(SCREEN_WIDTH - PLAYER_SIZE / 2, this.x));
        this.y = Math.max(PLAYER_SIZE / 2, Math.min(SCREEN_HEIGHT - PLAYER_SIZE / 2, this.y));
        
        // Regenerate energy slowly
        if (this.energy < this.maxEnergy) {
            this.energy += 10 * dt; // 10 energy per second
        }
    }
    
    move(direction, pressed) {
        switch (direction) {
            case "left":
                this.dx = pressed ? -1 : 0;
                break;
            case "right":
                this.dx = pressed ? 1 : 0;
                break;
            case "up":
                this.dy = pressed ? -1 : 0;
                break;
            case "down":
                this.dy = pressed ? 1 : 0;
                break;
        }
    }
    
    getGridPosition() {
        const gridX = Math.floor(this.x / GRID_SIZE);
        const gridY = Math.floor(this.y / GRID_SIZE);
        return [gridX, gridY];
    }
    
    getWorldPosition() {
        return [this.x, this.y];
    }
    
    addSeed(seedType, amount = 1) {
        if (seedType in this.seeds) {
            this.seeds[seedType] += amount;
        } else {
            this.seeds[seedType] = amount;
        }
    }
    
    useSeed(seedType) {
        if (this.hasSeed(seedType)) {
            this.seeds[seedType]--;
            if (this.seeds[seedType] <= 0) {
                delete this.seeds[seedType];
            }
            return true;
        }
        return false;
    }
    
    hasSeed(seedType) {
        return seedType in this.seeds && this.seeds[seedType] > 0;
    }
    
    addTool(toolName) {
        if (!this.tools.includes(toolName)) {
            this.tools.push(toolName);
        }
    }
    
    selectTool(toolName) {
        if (this.tools.includes(toolName)) {
            this.selectedTool = toolName;
        }
    }
    
    selectSeed(seedType) {
        if (this.hasSeed(seedType)) {
            this.selectedSeed = seedType;
        }
    }
    
    getSelectedSeed() {
        return this.selectedSeed;
    }
    
    getSelectedTool() {
        return this.selectedTool;
    }
    
    useEnergy(amount) {
        if (this.energy >= amount) {
            this.energy -= amount;
            return true;
        }
        return false;
    }
    
    addExperience(amount) {
        this.experience += amount;
        
        // Level up every 100 experience
        while (this.experience >= 100) {
            this.experience -= 100;
            this.level++;
            this.maxEnergy += 10;
            this.energy = this.maxEnergy;
        }
    }
    
    getInventorySummary() {
        return {
            seeds: { ...this.seeds },
            tools: [...this.tools],
            selectedTool: this.selectedTool,
            selectedSeed: this.selectedSeed,
            energy: this.energy,
            maxEnergy: this.maxEnergy,
            level: this.level,
            experience: this.experience
        };
    }
}
