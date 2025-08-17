// Shop Class - Manages available items and their costs
class Shop {
    constructor() {
        this.items = {
            "seeds": {
                "carrot": { name: "Carrot Seeds", cost: 10, description: "Fast-growing basic vegetable" },
                "tomato": { name: "Tomato Seeds", cost: 25, description: "Medium growth, good value" },
                "corn": { name: "Corn Seeds", cost: 40, description: "Slow growth, high value" },
                "strawberry": { name: "Strawberry Seeds", cost: 60, description: "Rare fruit, high mutation chance" },
                "sunflower": { name: "Sunflower Seeds", cost: 80, description: "Decorative, attracts beneficial insects" }
            },
            "tools": {
                "basic_watering_can": { name: "Basic Watering Can", cost: 0, description: "Basic watering tool (starter item)" },
                "advanced_watering_can": { name: "Advanced Watering Can", cost: 150, description: "Waters more efficiently" },
                "fertilizer_spreader": { name: "Fertilizer Spreader", cost: 200, description: "Applies fertilizer to multiple plants" },
                "sprinkler": { name: "Sprinkler System", cost: 500, description: "Automatically waters plants" },
                "pest_repellent": { name: "Pest Repellent", cost: 300, description: "Protects plants from pests" }
            },
            "fertilizers": {
                "basic_fertilizer": { name: "Basic Fertilizer", cost: 25, description: "Increases growth rate" },
                "premium_fertilizer": { name: "Premium Fertilizer", cost: 75, description: "Significantly increases growth and mutation chance" },
                "organic_fertilizer": { name: "Organic Fertilizer", cost: 100, description: "Improves soil quality over time" }
            },
            "expansions": {
                "garden_expansion": { name: "Garden Expansion", cost: 200, description: "Unlocks more garden space" },
                "greenhouse": { name: "Greenhouse", cost: 1000, description: "Protects plants from weather, faster growth" }
            }
        };
        
        // Unlock progression
        this.unlockedCategories = ["seeds", "tools"];
        this.unlockedItems = {
            "seeds": ["carrot"],
            "tools": ["basic_watering_can"],
            "fertilizers": [],
            "expansions": []
        };
        
        // Special offers and sales
        this.dailyDeals = {};
        this.saleMultiplier = 1.0;
    }
    
    getItem(category, itemName) {
        if (category in this.items && itemName in this.items[category]) {
            const item = { ...this.items[category][itemName] };
            
            // Apply sale multiplier
            if (itemName in this.dailyDeals) {
                item.cost = Math.floor(item.cost * this.dailyDeals[itemName]);
            } else {
                item.cost = Math.floor(item.cost * this.saleMultiplier);
            }
            
            return item;
        }
        return null;
    }
    
    getAvailableItems(category) {
        if (!this.unlockedCategories.includes(category)) {
            return [];
        }
        
        const available = [];
        for (const itemName of this.unlockedItems[category]) {
            const item = this.getItem(category, itemName);
            if (item) {
                available.push(item);
            }
        }
        
        return available;
    }
    
    getAllCategories() {
        return [...this.unlockedCategories];
    }
    
    unlockItem(category, itemName) {
        if (category in this.items && itemName in this.items[category]) {
            if (!this.unlockedCategories.includes(category)) {
                this.unlockedCategories.push(category);
            }
            
            if (!(category in this.unlockedItems)) {
                this.unlockedItems[category] = [];
            }
            
            if (!this.unlockedItems[category].includes(itemName)) {
                this.unlockedItems[category].push(itemName);
                return true;
            }
        }
        
        return false;
    }
    
    unlockCategory(category) {
        if (category in this.items && !this.unlockedCategories.includes(category)) {
            this.unlockedCategories.push(category);
            this.unlockedItems[category] = Object.keys(this.items[category]);
            return true;
        }
        return false;
    }
    
    setSale(multiplier) {
        this.saleMultiplier = Math.max(0.1, Math.min(1.0, multiplier));
    }
    
    addDailyDeal(itemName, discount) {
        this.dailyDeals[itemName] = Math.max(0.1, Math.min(1.0, 1.0 - discount));
    }
    
    clearDailyDeals() {
        this.dailyDeals = {};
    }
    
    getShopSummary() {
        return {
            unlockedCategories: [...this.unlockedCategories],
            unlockedItems: Object.fromEntries(
                Object.entries(this.unlockedItems).map(([cat, items]) => [cat, [...items]])
            ),
            saleMultiplier: this.saleMultiplier,
            dailyDeals: { ...this.dailyDeals }
        };
    }
    
    canAffordItem(category, itemName, money) {
        const item = this.getItem(category, itemName);
        if (!item) {
            return false;
        }
        return money >= item.cost;
    }
    
    getItemCost(category, itemName) {
        const item = this.getItem(category, itemName);
        return item ? item.cost : 0;
    }
    
    getRecommendedItems(money, category = null) {
        const recommended = [];
        
        const categories = category ? [category] : this.unlockedCategories;
        
        for (const cat of categories) {
            if (!this.unlockedCategories.includes(cat)) {
                continue;
            }
            
            for (const itemName of this.unlockedItems[cat]) {
                if (this.canAffordItem(cat, itemName, money)) {
                    const item = this.getItem(cat, itemName);
                    if (item) {
                        recommended.push(item);
                    }
                }
            }
        }
        
        // Sort by cost (cheapest first)
        recommended.sort((a, b) => a.cost - b.cost);
        return recommended;
    }
}
