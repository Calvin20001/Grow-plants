// Garden Class - Manages the grid-based garden system and plant placement
class Garden {
    constructor() {
        this.width = GRID_WIDTH;
        this.height = GRID_HEIGHT;
        
        // Grid system
        this.grid = Array(this.height).fill().map(() => Array(this.width).fill(null));
        this.plants = new Map(); // (x, y) -> Plant mapping
        
        // Garden state
        this.soilQuality = Array(this.height).fill().map(() => Array(this.width).fill(1.0));
        this.waterLevels = Array(this.height).fill().map(() => Array(this.width).fill(0));
        this.fertilizerLevels = Array(this.height).fill().map(() => Array(this.width).fill(0));
        
        // Garden expansions
        this.expansions = 1;
        this.maxExpansions = 3;
        
        // Weather effects
        this.rainTimer = 0.0;
        this.pestInfestation = false;
        this.pestTimer = 0.0;
        
        // Initialize starting garden area
        this.initializeGarden();
    }
    
    initializeGarden() {
        // Start with a 5x5 garden in the center
        const startX = Math.floor(this.width / 2) - 2;
        const startY = Math.floor(this.height / 2) - 2;
        
        for (let y = startY; y < startY + 5; y++) {
            for (let x = startX; x < startX + 5; x++) {
                if (x >= 0 && x < this.width && y >= 0 && y < this.height) {
                    this.soilQuality[y][x] = 1.0;
                    this.waterLevels[y][x] = 2;
                    this.fertilizerLevels[y][x] = 0;
                }
            }
        }
    }
    
    update(dt) {
        // Update all plants
        for (const plant of this.plants.values()) {
            plant.update(dt);
        }
        
        // Update weather effects
        if (this.rainTimer > 0) {
            this.rainTimer -= dt;
            if (this.rainTimer <= 0) {
                this.endRainEffect();
            }
        }
        
        // Update pest infestation
        if (this.pestInfestation) {
            this.pestTimer += dt;
            if (this.pestTimer >= 30.0) { // Pests last 30 seconds
                this.endPestInfestation();
            }
        }
    }
    
    plantSeed(x, y, seedType) {
        if (!this.isValidPosition(x, y)) {
            return false;
        }
        
        if (this.grid[y][x] !== null) {
            return false; // Position already occupied
        }
        
        if (!this.isPlantableSoil(x, y)) {
            return false; // Not plantable soil
        }
        
        // Create new plant
        const plant = new Plant(seedType, x, y);
        this.grid[y][x] = plant;
        this.plants.set(`${x},${y}`, plant);
        
        // Apply soil quality effects
        const soilQuality = this.soilQuality[y][x];
        if (soilQuality < 0.5) {
            plant.growthProgress *= 0.8; // Slower growth on poor soil
        }
        
        return true;
    }
    
    waterPlant(x, y) {
        if (!this.isValidPosition(x, y)) {
            return false;
        }
        
        const plant = this.grid[y][x];
        if (plant === null) {
            return false;
        }
        
        // Water the plant
        if (plant.water()) {
            // Update soil water level
            this.waterLevels[y][x] = Math.min(5, this.waterLevels[y][x] + 1);
            return true;
        }
        
        return false;
    }
    
    fertilizePlant(x, y) {
        if (!this.isValidPosition(x, y)) {
            return false;
        }
        
        const plant = this.grid[y][x];
        if (plant === null) {
            return false;
        }
        
        // Apply fertilizer
        if (plant.fertilize()) {
            // Update soil fertilizer level
            this.fertilizerLevels[y][x] = Math.min(3, this.fertilizerLevels[y][x] + 1);
            return true;
        }
        
        return false;
    }
    
    getPlant(x, y) {
        if (!this.isValidPosition(x, y)) {
            return null;
        }
        return this.grid[y][x];
    }
    
    removePlant(x, y) {
        if (!this.isValidPosition(x, y)) {
            return false;
        }
        
        if (this.grid[y][x] !== null) {
            const plant = this.grid[y][x];
            this.plants.delete(`${x},${y}`);
            this.grid[y][x] = null;
            
            // Improve soil quality slightly when plant is harvested
            this.soilQuality[y][x] = Math.min(1.5, this.soilQuality[y][x] + 0.1);
            
            return true;
        }
        
        return false;
    }
    
    expand() {
        if (this.expansions >= this.maxExpansions) {
            return false;
        }
        
        this.expansions++;
        
        // Increase plantable area
        const expansionSize = 2;
        const centerX = Math.floor(this.width / 2);
        const centerY = Math.floor(this.height / 2);
        
        for (let y = centerY - expansionSize; y <= centerY + expansionSize; y++) {
            for (let x = centerX - expansionSize; x <= centerX + expansionSize; x++) {
                if (x >= 0 && x < this.width && y >= 0 && y < this.height) {
                    if (this.soilQuality[y][x] === 0) {
                        this.soilQuality[y][x] = 0.8;
                        this.waterLevels[y][x] = 1;
                    }
                }
            }
        }
        
        return true;
    }
    
    applyRainEffect() {
        this.rainTimer = 20.0; // Rain lasts 20 seconds
        
        // Water all plants
        for (const plant of this.plants.values()) {
            plant.water();
        }
        
        // Increase soil water levels
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.isPlantableSoil(x, y)) {
                    this.waterLevels[y][x] = Math.min(5, this.waterLevels[y][x] + 2);
                }
            }
        }
    }
    
    endRainEffect() {
        this.rainTimer = 0.0;
    }
    
    triggerPestInfestation() {
        if (!this.pestInfestation) {
            this.pestInfestation = true;
            this.pestTimer = 0.0;
            
            // Randomly destroy some plants
            const plantPositions = Array.from(this.plants.keys());
            if (plantPositions.length > 0) {
                const numToDestroy = Math.min(3, plantPositions.length);
                const positionsToDestroy = this.shuffleArray(plantPositions).slice(0, numToDestroy);
                
                for (const pos of positionsToDestroy) {
                    const [x, y] = pos.split(',').map(Number);
                    this.removePlant(x, y);
                }
            }
        }
    }
    
    endPestInfestation() {
        this.pestInfestation = false;
        this.pestTimer = 0.0;
    }
    
    isValidPosition(x, y) {
        return x >= 0 && x < this.width && y >= 0 && y < this.height;
    }
    
    isPlantableSoil(x, y) {
        return this.soilQuality[y][x] > 0;
    }
    
    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }
    
    getGardenSummary() {
        return {
            width: this.width,
            height: this.height,
            expansions: this.expansions,
            maxExpansions: this.maxExpansions,
            totalPlants: this.plants.size,
            plantableTiles: this.soilQuality.flat().filter(quality => quality > 0).length,
            weather: {
                rainTimer: this.rainTimer,
                pestInfestation: this.pestInfestation,
                pestTimer: this.pestTimer
            }
        };
    }
    
    getPlantPositions() {
        return Array.from(this.plants.keys()).map(pos => {
            const [x, y] = pos.split(',').map(Number);
            return [x, y];
        });
    }
    
    getPlantablePositions() {
        const positions = [];
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.isPlantableSoil(x, y)) {
                    positions.push([x, y]);
                }
            }
        }
        return positions;
    }
}
