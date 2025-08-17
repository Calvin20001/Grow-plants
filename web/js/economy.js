// Economy Class - Manages money, market prices, and economic systems
class Economy {
    constructor() {
        this.money = STARTING_MONEY;
        this.totalEarned = 0;
        this.totalSpent = 0;
        
        // Market prices and fluctuations
        this.basePrices = {
            "carrot": 15,
            "tomato": 25,
            "corn": 35,
            "strawberry": 50,
            "sunflower": 40
        };
        
        this.currentPrices = { ...this.basePrices };
        this.priceMultipliers = {};
        for (const plant in this.basePrices) {
            this.priceMultipliers[plant] = 1.0;
        }
        
        // Market events
        this.marketBoom = false;
        this.marketBoomTimer = 0.0;
        this.marketCrash = false;
        this.marketCrashTimer = 0.0;
        
        // Price history for trends
        this.priceHistory = {};
        for (const plant in this.basePrices) {
            this.priceHistory[plant] = [];
        }
        this.maxHistoryLength = 10;
        
        // Economic milestones
        this.milestones = {
            100: "First Harvest",
            500: "Small Farmer",
            1000: "Established Gardener",
            2500: "Plant Master",
            5000: "Garden Empire",
            10000: "Plant Legend"
        };
        this.achievedMilestones = new Set();
    }
    
    update(dt) {
        // Update market events
        if (this.marketBoom) {
            this.marketBoomTimer -= dt;
            if (this.marketBoomTimer <= 0) {
                this.endMarketBoom();
            }
        }
        
        if (this.marketCrash) {
            this.marketCrashTimer -= dt;
            if (this.marketCrashTimer <= 0) {
                this.endMarketCrash();
            }
        }
        
        // Check milestones
        this.checkMilestones();
    }
    
    addMoney(amount) {
        this.money += amount;
        this.totalEarned += amount;
    }
    
    spendMoney(amount) {
        if (this.money >= amount) {
            this.money -= amount;
            this.totalSpent += amount;
            return true;
        }
        return false;
    }
    
    canAfford(cost) {
        return this.money >= cost;
    }
    
    getBalance() {
        return this.money;
    }
    
    calculatePlantValue(plant) {
        let baseValue = this.currentPrices[plant.plantType] || 20;
        
        // Apply plant-specific modifiers
        let value = baseValue;
        
        // Stage bonus (more mature plants worth more)
        const stageBonus = 1.0 + (plant.currentStage * 0.1);
        value *= stageBonus;
        
        // Mutation bonus
        if (plant.isMutated) {
            value *= 2.0; // Mutated plants worth double
        }
        
        // Care bonus
        let careBonus = 1.0;
        if (plant.fertilized) {
            careBonus += 0.2;
        }
        if (plant.waterLevel >= plant.maxWaterLevel) {
            careBonus += 0.1;
        }
        
        value *= careBonus;
        
        // Market condition bonus
        if (this.marketBoom) {
            value = Math.floor(value * 1.5);
        } else if (this.marketCrash) {
            value = Math.floor(value * 0.7);
        }
        
        return Math.max(1, Math.floor(value));
    }
    
    updateMarketPrices() {
        for (const plantType in this.basePrices) {
            // Random price fluctuation
            const fluctuation = (Math.random() - 0.5) * 0.2; // -0.1 to 0.1
            this.priceMultipliers[plantType] += fluctuation;
            
            // Keep multipliers within reasonable bounds
            this.priceMultipliers[plantType] = Math.max(0.5, Math.min(2.0, this.priceMultipliers[plantType]));
            
            // Update current price
            this.currentPrices[plantType] = Math.floor(this.basePrices[plantType] * this.priceMultipliers[plantType]);
            
            // Add to price history
            this.priceHistory[plantType].push(this.currentPrices[plantType]);
            if (this.priceHistory[plantType].length > this.maxHistoryLength) {
                this.priceHistory[plantType].shift();
            }
        }
    }
    
    triggerMarketBoom() {
        if (!this.marketBoom) {
            this.marketBoom = true;
            this.marketBoomTimer = 60.0; // Boom lasts 1 minute
            
            // Increase all prices
            for (const plantType in this.currentPrices) {
                this.currentPrices[plantType] = Math.floor(this.currentPrices[plantType] * 1.5);
            }
        }
    }
    
    triggerMarketCrash() {
        if (!this.marketCrash) {
            this.marketCrash = true;
            this.marketCrashTimer = 45.0; // Crash lasts 45 seconds
            
            // Decrease all prices
            for (const plantType in this.currentPrices) {
                this.currentPrices[plantType] = Math.floor(this.currentPrices[plantType] * 0.7);
            }
        }
    }
    
    endMarketBoom() {
        this.marketBoom = false;
        this.marketBoomTimer = 0.0;
        
        // Reset prices to normal
        for (const plantType in this.currentPrices) {
            this.currentPrices[plantType] = Math.floor(this.basePrices[plantType] * this.priceMultipliers[plantType]);
        }
    }
    
    endMarketCrash() {
        this.marketCrash = false;
        this.marketCrashTimer = 0.0;
        
        // Reset prices to normal
        for (const plantType in this.currentPrices) {
            this.currentPrices[plantType] = Math.floor(this.basePrices[plantType] * this.priceMultipliers[plantType]);
        }
    }
    
    checkMilestones() {
        for (const milestoneAmount of Object.keys(this.milestones).map(Number).sort((a, b) => a - b)) {
            if (this.totalEarned >= milestoneAmount && !this.achievedMilestones.has(milestoneAmount)) {
                this.achievedMilestones.add(milestoneAmount);
                // Could trigger achievement notification here
            }
        }
    }
    
    getMarketSummary() {
        return {
            currentPrices: { ...this.currentPrices },
            basePrices: { ...this.basePrices },
            priceMultipliers: { ...this.priceMultipliers },
            marketBoom: this.marketBoom,
            marketCrash: this.marketCrash,
            boomTimer: this.marketBoomTimer,
            crashTimer: this.marketCrashTimer
        };
    }
    
    getEconomicSummary() {
        return {
            money: this.money,
            totalEarned: this.totalEarned,
            totalSpent: this.totalSpent,
            netWorth: this.money,
            achievedMilestones: Array.from(this.achievedMilestones),
            nextMilestone: this.getNextMilestone()
        };
    }
    
    getNextMilestone() {
        for (const milestoneAmount of Object.keys(this.milestones).map(Number).sort((a, b) => a - b)) {
            if (milestoneAmount > this.totalEarned) {
                return `${this.milestones[milestoneAmount]} (${milestoneAmount - this.totalEarned} more needed)`;
            }
        }
        return "All milestones achieved!";
    }
    
    getPriceTrend(plantType) {
        if (!this.priceHistory[plantType] || this.priceHistory[plantType].length < 2) {
            return "stable";
        }
        
        const history = this.priceHistory[plantType];
        if (history.length >= 2) {
            const recentChange = history[history.length - 1] - history[history.length - 2];
            if (recentChange > 0) {
                return "rising";
            } else if (recentChange < 0) {
                return "falling";
            }
        }
        
        return "stable";
    }
    
    getBestInvestment() {
        let bestPlant = null;
        let bestRatio = 0;
        
        for (const [plantType, currentPrice] of Object.entries(this.currentPrices)) {
            const basePrice = this.basePrices[plantType];
            const ratio = currentPrice / basePrice;
            
            if (ratio > bestRatio) {
                bestRatio = ratio;
                bestPlant = plantType;
            }
        }
        
        return bestPlant || "carrot";
    }
}
