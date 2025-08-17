// Renderer Class - Handles all game graphics and UI rendering
class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Colors for different soil types
        this.soilColors = {
            0.0: COLORS.BLACK,      // Unusable
            0.5: COLORS.LIGHT_BROWN, // Poor soil
            1.0: COLORS.BROWN,      // Normal soil
            1.5: COLORS.DARK_GREEN  // Rich soil
        };
    }
    
    renderGarden(garden) {
        for (let y = 0; y < garden.height; y++) {
            for (let x = 0; x < garden.width; x++) {
                // Calculate screen position
                const screenX = x * GRID_SIZE;
                const screenY = y * GRID_SIZE;
                
                // Get soil quality
                const soilQuality = garden.soilQuality[y][x];
                
                // Determine soil color
                const soilColor = this.getSoilColor(soilQuality);
                
                // Draw soil tile
                this.ctx.fillStyle = soilColor;
                this.ctx.fillRect(screenX, screenY, GRID_SIZE, GRID_SIZE);
                
                // Draw grid lines
                this.ctx.strokeStyle = COLORS.GRAY;
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(screenX, screenY, GRID_SIZE, GRID_SIZE);
                
                // Draw water level indicator
                if (garden.waterLevels[y][x] > 0) {
                    const waterAlpha = Math.min(1.0, garden.waterLevels[y][x] * 0.1);
                    this.ctx.fillStyle = `rgba(173, 216, 230, ${waterAlpha})`;
                    this.ctx.fillRect(screenX, screenY, GRID_SIZE, GRID_SIZE);
                }
                
                // Draw fertilizer indicator
                if (garden.fertilizerLevels[y][x] > 0) {
                    const fertColor = garden.fertilizerLevels[y][x] >= 2 ? COLORS.GREEN : COLORS.LIGHT_GREEN;
                    const fertSize = Math.min(GRID_SIZE / 4, garden.fertilizerLevels[y][x] * 2);
                    const fertX = screenX + (GRID_SIZE - fertSize) / 2;
                    const fertY = screenY + (GRID_SIZE - fertSize) / 2;
                    
                    this.ctx.fillStyle = fertColor;
                    this.ctx.beginPath();
                    this.ctx.arc(fertX + fertSize / 2, fertY + fertSize / 2, fertSize / 2, 0, Math.PI * 2);
                    this.ctx.fill();
                }
            }
        }
    }
    
    renderPlant(plant) {
        // Get plant visual properties
        const props = plant.getVisualProperties();
        
        // Calculate screen position
        const screenX = (plant.x * GRID_SIZE) + (GRID_SIZE / 2);
        const screenY = (plant.y * GRID_SIZE) + (GRID_SIZE / 2);
        
        // Calculate plant size
        const plantSize = Math.floor(props.size * GRID_SIZE * 0.8);
        
        // Draw plant based on stage
        const stage = props.stage;
        const color = props.color;
        
        switch (stage) {
            case "seed":
                // Draw seed
                this.ctx.fillStyle = COLORS.BROWN;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, plantSize / 2, 0, Math.PI * 2);
                this.ctx.fill();
                break;
                
            case "sprout":
                // Draw sprout
                this.ctx.fillStyle = COLORS.LIGHT_GREEN;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, plantSize / 2, 0, Math.PI * 2);
                this.ctx.fill();
                
                // Draw stem
                this.ctx.strokeStyle = COLORS.GREEN;
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(screenX, screenY);
                this.ctx.lineTo(screenX, screenY - plantSize / 2);
                this.ctx.stroke();
                break;
                
            case "small_plant":
                // Draw small plant
                this.ctx.fillStyle = color;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, plantSize / 2, 0, Math.PI * 2);
                this.ctx.fill();
                
                // Draw leaves
                for (let i = 0; i < 3; i++) {
                    const angle = (i * 120) * Math.PI / 180;
                    const leafX = screenX + Math.cos(angle) * plantSize * 0.3;
                    const leafY = screenY + Math.sin(angle) * plantSize * 0.3;
                    
                    this.ctx.fillStyle = COLORS.GREEN;
                    this.ctx.beginPath();
                    this.ctx.arc(leafX, leafY, plantSize / 4, 0, Math.PI * 2);
                    this.ctx.fill();
                }
                break;
                
            case "mature_plant":
                // Draw mature plant
                this.ctx.fillStyle = color;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, plantSize / 2, 0, Math.PI * 2);
                this.ctx.fill();
                
                // Draw multiple leaves
                for (let i = 0; i < 6; i++) {
                    const angle = (i * 60) * Math.PI / 180;
                    const leafX = screenX + Math.cos(angle) * plantSize * 0.4;
                    const leafY = screenY + Math.sin(angle) * plantSize * 0.4;
                    
                    this.ctx.fillStyle = COLORS.GREEN;
                    this.ctx.beginPath();
                    this.ctx.arc(leafX, leafY, plantSize / 3, 0, Math.PI * 2);
                    this.ctx.fill();
                }
                break;
                
            case "harvestable":
                // Draw harvestable plant with shine effect
                this.ctx.fillStyle = color;
                this.ctx.beginPath();
                this.ctx.arc(screenX, screenY, plantSize / 2, 0, Math.PI * 2);
                this.ctx.fill();
                
                // Draw shine effect
                const shineSize = plantSize / 3;
                this.ctx.fillStyle = COLORS.WHITE;
                this.ctx.beginPath();
                this.ctx.arc(screenX - shineSize / 3, screenY - shineSize / 3, shineSize / 2, 0, Math.PI * 2);
                this.ctx.fill();
                break;
        }
        
        // Draw mutation indicator
        if (props.mutated) {
            this.ctx.strokeStyle = COLORS.PURPLE;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.arc(screenX, screenY, plantSize / 2 + 2, 0, Math.PI * 2);
            this.ctx.stroke();
        }
        
        // Draw water level indicator
        if (props.waterLevel < props.maxWaterLevel) {
            const waterBarWidth = GRID_SIZE - 4;
            const waterBarHeight = 4;
            const waterBarX = screenX - waterBarWidth / 2;
            const waterBarY = screenY - plantSize / 2 - 8;
            
            // Background bar
            this.ctx.fillStyle = COLORS.GRAY;
            this.ctx.fillRect(waterBarX, waterBarY, waterBarWidth, waterBarHeight);
            
            // Water level
            const waterFill = (props.waterLevel / props.maxWaterLevel) * waterBarWidth;
            this.ctx.fillStyle = COLORS.BLUE;
            this.ctx.fillRect(waterBarX, waterBarY, waterFill, waterBarHeight);
        }
    }
    
    renderPlayer(player) {
        // Draw player as a simple circle
        this.ctx.fillStyle = COLORS.BLUE;
        this.ctx.beginPath();
        this.ctx.arc(player.x, player.y, PLAYER_SIZE / 2, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw player outline
        this.ctx.strokeStyle = COLORS.WHITE;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(player.x, player.y, PLAYER_SIZE / 2, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Draw direction indicator
        if (player.dx !== 0 || player.dy !== 0) {
            const directionX = player.dx * 8;
            const directionY = player.dy * 8;
            
            this.ctx.strokeStyle = COLORS.WHITE;
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.moveTo(player.x, player.y);
            this.ctx.lineTo(player.x + directionX, player.y + directionY);
            this.ctx.stroke();
        }
    }
    
    renderText(text, x, y, color, size, center = false, alpha = 1.0) {
        this.ctx.save();
        this.ctx.globalAlpha = alpha;
        this.ctx.fillStyle = color;
        this.ctx.font = `${size}px Arial`;
        this.ctx.textAlign = center ? 'center' : 'left';
        this.ctx.textBaseline = 'middle';
        
        if (center) {
            this.ctx.fillText(text, x, y);
        } else {
            this.ctx.fillText(text, x, y);
        }
        
        this.ctx.restore();
    }
    
    renderShop(shop, economy) {
        // Background
        this.ctx.fillStyle = COLORS.DARK_GREEN;
        this.ctx.fillRect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200);
        
        // Title
        this.renderText("SHOP", SCREEN_WIDTH / 2, 130, COLORS.WHITE, 32, true);
        
        // Money display
        const moneyText = `Money: $${economy.money}`;
        this.renderText(moneyText, SCREEN_WIDTH / 2, 170, COLORS.YELLOW, 24, true);
        
        // Categories
        const categories = shop.getAllCategories();
        let yOffset = 220;
        
        for (const category of categories) {
            // Category header
            this.renderText(category.toUpperCase(), 150, yOffset, COLORS.WHITE, 20);
            yOffset += 30;
            
            // Items in category
            const items = shop.getAvailableItems(category);
            for (const item of items) {
                const itemText = `${item.name} - ${item.cost} coins`;
                this.renderText(itemText, 170, yOffset, COLORS.LIGHT_GRAY, 18);
                yOffset += 25;
            }
            
            yOffset += 20;
        }
        
        // Close instruction
        this.renderText("Press ESC to close", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120, COLORS.WHITE, 18, true);
    }
    
    renderInventory(player) {
        // Background
        this.ctx.fillStyle = COLORS.DARK_GREEN;
        this.ctx.fillRect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200);
        
        // Title
        this.renderText("INVENTORY", SCREEN_WIDTH / 2, 130, COLORS.WHITE, 32, true);
        
        // Player stats
        const stats = player.getInventorySummary();
        let yOffset = 180;
        
        // Seeds
        this.renderText("SEEDS:", 150, yOffset, COLORS.WHITE, 20);
        yOffset += 25;
        for (const [seedType, amount] of Object.entries(stats.seeds)) {
            const seedText = `${seedType.charAt(0).toUpperCase() + seedType.slice(1)}: ${amount}`;
            this.renderText(seedText, 170, yOffset, COLORS.LIGHT_GRAY, 18);
            yOffset += 20;
        }
        
        yOffset += 20;
        
        // Tools
        this.renderText("TOOLS:", 150, yOffset, COLORS.WHITE, 20);
        yOffset += 25;
        for (const tool of stats.tools) {
            const toolText = tool.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            const color = tool === stats.selectedTool ? COLORS.YELLOW : COLORS.LIGHT_GRAY;
            this.renderText(toolText, 170, yOffset, color, 18);
            yOffset += 20;
        }
        
        yOffset += 20;
        
        // Stats
        this.renderText(`Level: ${stats.level}`, 150, yOffset, COLORS.WHITE, 20);
        yOffset += 25;
        this.renderText(`Experience: ${stats.experience}/100`, 150, yOffset, COLORS.WHITE, 20);
        yOffset += 25;
        this.renderText(`Energy: ${stats.energy}/${stats.maxEnergy}`, 150, yOffset, COLORS.WHITE, 20);
        
        // Close instruction
        this.renderText("Press ESC to close", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120, COLORS.WHITE, 18, true);
    }
    
    renderHelp() {
        // Background
        this.ctx.fillStyle = COLORS.DARK_GREEN;
        this.ctx.fillRect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200);
        
        // Title
        this.renderText("HELP & CONTROLS", SCREEN_WIDTH / 2, 130, COLORS.WHITE, 32, true);
        
        // Controls
        const controls = [
            "WASD or Arrow Keys: Move player",
            "Space: Interact with plants/soil",
            "E: Open shop",
            "Q: Open inventory",
            "H: Show this help",
            "ESC: Pause game or close menus",
            "",
            "GAMEPLAY:",
            "• Plant seeds in soil tiles",
            "• Water plants regularly",
            "• Use fertilizer for better growth",
            "• Harvest mature plants for money",
            "• Buy upgrades in the shop",
            "• Expand your garden area"
        ];
        
        let yOffset = 180;
        for (const control of controls) {
            if (control === "") {
                yOffset += 20;
                continue;
            }
            this.renderText(control, 150, yOffset, COLORS.LIGHT_GRAY, 18);
            yOffset += 25;
        }
        
        // Close instruction
        this.renderText("Press ESC to close", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120, COLORS.WHITE, 18, true);
    }
    
    renderPauseScreen() {
        // Semi-transparent overlay
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        
        // Pause text
        this.renderText("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, COLORS.WHITE, 48, true);
        this.renderText("Press ESC to resume", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20, COLORS.WHITE, 24, true);
    }
    
    renderNotifications(notifications) {
        let yOffset = 200;
        for (const notification of notifications) {
            if (notification.timer > 0) {
                const alpha = Math.min(1.0, notification.timer / 3.0);
                this.renderText(
                    notification.message,
                    SCREEN_WIDTH / 2,
                    yOffset,
                    COLORS.WHITE,
                    20,
                    true,
                    alpha
                );
                yOffset += 30;
            }
        }
    }
    
    getSoilColor(quality) {
        if (quality <= 0.0) return this.soilColors[0.0];
        if (quality <= 0.5) return this.soilColors[0.5];
        if (quality <= 1.0) return this.soilColors[1.0];
        return this.soilColors[1.5];
    }
    
    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}
