// Plant Class - Handles individual plant growth, mutations, and states
class Plant {
    constructor(plantType, x, y) {
        this.plantType = plantType;
        this.x = x;
        this.y = y;
        
        // Get plant data from constants
        const plantData = PLANT_TYPES[plantType] || PLANT_TYPES["carrot"];
        this.name = plantData.name;
        this.baseGrowthTime = plantData.growth_time;
        this.waterNeed = plantData.water_need;
        this.baseValue = plantData.base_value;
        this.baseMutationChance = plantData.mutation_chance;
        this.baseColor = plantData.color;
        
        // Growth state
        this.currentStage = 0; // Index into GROWTH_STAGES
        this.growthProgress = 0.0; // 0.0 to 1.0
        this.growthTimer = 0.0;
        this.stageTimer = 0.0;
        
        // Water and care
        this.waterLevel = 0;
        this.maxWaterLevel = this.waterNeed;
        this.lastWatered = 0.0;
        this.fertilized = false;
        
        // Mutations
        this.mutations = [];
        this.isMutated = false;
        this.mutationMultiplier = 1.0;
        
        // Visual properties
        this.sizeMultiplier = 1.0;
        this.colorVariants = [];
        
        // Check for initial mutation
        this.checkInitialMutation();
    }
    
    update(dt) {
        this.growthTimer += dt;
        this.stageTimer += dt;
        
        // Calculate growth rate
        const growthRate = this.calculateGrowthRate();
        
        // Update growth progress
        this.growthProgress += growthRate * dt;
        
        // Check for stage advancement
        if (this.growthProgress >= 1.0 && this.currentStage < GROWTH_STAGES.length - 1) {
            this.advanceStage();
        }
        
        // Reduce water over time
        if (this.growthTimer - this.lastWatered > 10.0) { // Water depletes every 10 seconds
            this.waterLevel = Math.max(0, this.waterLevel - 1);
        }
    }
    
    calculateGrowthRate() {
        const baseRate = 1.0 / this.baseGrowthTime;
        
        // Water bonus
        let waterBonus = 1.0;
        if (this.waterLevel >= this.maxWaterLevel) {
            waterBonus = 1.0 + WATERING_BONUS;
        } else if (this.waterLevel === 0) {
            waterBonus = 0.5; // Slow growth when dry
        }
        
        // Fertilizer bonus
        const fertilizerBonus = this.fertilized ? (1.0 + FERTILIZER_BONUS) : 1.0;
        
        return baseRate * waterBonus * fertilizerBonus;
    }
    
    advanceStage() {
        this.currentStage++;
        this.growthProgress = 0.0;
        this.stageTimer = 0.0;
        
        // Check for mutations on stage advancement
        if (this.currentStage > 1) { // Don't mutate on seed stage
            this.checkMutation();
        }
    }
    
    checkInitialMutation() {
        if (Math.random() < this.baseMutationChance * 0.1) { // Lower chance for initial
            this.applyMutation("early_growth");
        }
    }
    
    checkMutation() {
        if (this.isMutated) {
            return; // Already mutated
        }
        
        let mutationChance = this.baseMutationChance;
        
        // Increase chance with fertilizer
        if (this.fertilized) {
            mutationChance *= 1.5;
        }
        
        // Increase chance with good care
        if (this.waterLevel >= this.maxWaterLevel) {
            mutationChance *= 1.2;
        }
        
        if (Math.random() < mutationChance) {
            this.applyMutation("growth_spurt");
        }
    }
    
    applyMutation(mutationType) {
        this.isMutated = true;
        this.mutations.push(mutationType);
        
        switch (mutationType) {
            case "growth_spurt":
                this.mutationMultiplier = 1.5;
                this.sizeMultiplier = 1.3;
                break;
            case "early_growth":
                this.mutationMultiplier = 1.2;
                this.growthProgress += 0.3;
                break;
            case "rare_color":
                this.colorVariants.push("rare");
                this.mutationMultiplier = 2.0;
                break;
            case "giant":
                this.sizeMultiplier = 2.0;
                this.mutationMultiplier = 3.0;
                break;
        }
    }
    
    water() {
        if (this.waterLevel < this.maxWaterLevel) {
            this.waterLevel = Math.min(this.maxWaterLevel, this.waterLevel + 1);
            this.lastWatered = this.growthTimer;
            return true;
        }
        return false;
    }
    
    fertilize() {
        if (!this.fertilized) {
            this.fertilized = true;
            return true;
        }
        return false;
    }
    
    getCurrentStage() {
        return GROWTH_STAGES[this.currentStage];
    }
    
    isHarvestable() {
        return this.currentStage === GROWTH_STAGES.length - 1;
    }
    
    getValue() {
        let baseValue = this.baseValue;
        
        // Stage multiplier
        const stageMultiplier = 1.0 + (this.currentStage * 0.2);
        
        // Mutation multiplier
        const mutationMultiplier = this.mutationMultiplier;
        
        // Care bonus
        let careBonus = 1.0;
        if (this.fertilized) {
            careBonus += 0.3;
        }
        if (this.waterLevel >= this.maxWaterLevel) {
            careBonus += 0.2;
        }
        
        return Math.max(1, Math.floor(baseValue * stageMultiplier * mutationMultiplier * careBonus));
    }
    
    getVisualProperties() {
        const stage = this.getCurrentStage();
        
        // Base size based on stage
        const baseSize = 0.3 + (this.currentStage * 0.15);
        const finalSize = baseSize * this.sizeMultiplier;
        
        // Color variations
        let color = this.baseColor;
        if (this.colorVariants.includes("rare")) {
            color = COLORS.PURPLE; // Rare color
        }
        
        return {
            size: finalSize,
            color: color,
            stage: stage,
            waterLevel: this.waterLevel,
            maxWaterLevel: this.maxWaterLevel,
            fertilized: this.fertilized,
            mutated: this.isMutated
        };
    }
    
    getStatusSummary() {
        return {
            type: this.plantType,
            name: this.name,
            stage: this.getCurrentStage(),
            growthProgress: this.growthProgress,
            waterLevel: this.waterLevel,
            maxWaterLevel: this.maxWaterLevel,
            fertilized: this.fertilized,
            mutated: this.isMutated,
            mutations: [...this.mutations],
            value: this.getValue(),
            position: [this.x, this.y]
        };
    }
}
