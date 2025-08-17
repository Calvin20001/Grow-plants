// Main game initialization and loop
let game, renderer, canvas;
let lastTime = 0;
let running = true;

// UI functions
function closeShop() {
    game.showShop = false;
}

function closeInventory() {
    game.showInventory = false;
}

function closeHelp() {
    game.showHelp = false;
}

function updateUI() {
    // Update money display
    document.getElementById('money').textContent = `Money: $${game.economy.money}`;
    
    // Update day display
    document.getElementById('day').textContent = `Day: ${game.day}`;
    
    // Update weather display
    document.getElementById('weather').textContent = `Weather: ${game.weather.charAt(0).toUpperCase() + game.weather.slice(1)}`;
    
    // Update selected items
    const selectedSeed = game.player.getSelectedSeed();
    const selectedTool = game.player.getSelectedTool();
    document.getElementById('selected').textContent = `Seed: ${selectedSeed.charAt(0).toUpperCase() + selectedSeed.slice(1)} | Tool: ${selectedTool.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}`;
    
    // Update shop content
    if (game.showShop) {
        updateShopUI();
    }
    
    // Update inventory content
    if (game.showInventory) {
        updateInventoryUI();
    }
    
    // Update help content
    if (game.showHelp) {
        updateHelpUI();
    }
}

function updateShopUI() {
    const shopContent = document.getElementById('shopContent');
    const categories = game.shop.getAllCategories();
    
    let html = '';
    for (const category of categories) {
        html += `<h3>${category.toUpperCase()}</h3>`;
        const items = game.shop.getAvailableItems(category);
        for (const item of items) {
            const affordable = game.economy.canAfford(item.cost);
            html += `
                <div style="margin: 10px 0; padding: 10px; background: ${affordable ? '#4a6a4a' : '#333'}; border-radius: 5px;">
                    <strong>${item.name}</strong> - ${item.cost} coins
                    <br><small>${item.description}</small>
                    ${affordable ? `<button onclick="purchaseItem('${category}', '${item.name}')" style="float: right;">Buy</button>` : '<span style="float: right; color: #666;">Can\'t afford</span>'}
                </div>
            `;
        }
    }
    
    shopContent.innerHTML = html;
}

function updateInventoryUI() {
    const inventoryContent = document.getElementById('inventoryContent');
    const stats = game.player.getInventorySummary();
    
    let html = `
        <h3>SEEDS:</h3>
        <div style="margin: 10px 0;">
    `;
    
    for (const [seedType, amount] of Object.entries(stats.seeds)) {
        const isSelected = seedType === stats.selectedSeed;
        html += `
            <div style="margin: 5px 0; padding: 5px; background: ${isSelected ? '#4a6a4a' : '#333'}; border-radius: 3px;">
                ${seedType.charAt(0).toUpperCase() + seedType.slice(1)}: ${amount}
                ${isSelected ? ' (Selected)' : `<button onclick="selectSeed('${seedType}')" style="float: right;">Select</button>`}
            </div>
        `;
    }
    
    html += `
        </div>
        <h3>TOOLS:</h3>
        <div style="margin: 10px 0;">
    `;
    
    for (const tool of stats.tools) {
        const isSelected = tool === stats.selectedTool;
        html += `
            <div style="margin: 5px 0; padding: 5px; background: ${isSelected ? '#4a6a4a' : '#333'}; border-radius: 3px;">
                ${tool.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                ${isSelected ? ' (Selected)' : `<button onclick="selectTool('${tool}')" style="float: right;">Select</button>`}
            </div>
        `;
    }
    
    html += `
        </div>
        <h3>STATS:</h3>
        <div style="margin: 10px 0;">
            <div>Level: ${stats.level}</div>
            <div>Experience: ${stats.experience}/100</div>
            <div>Energy: ${stats.energy}/${stats.maxEnergy}</div>
        </div>
    `;
    
    inventoryContent.innerHTML = html;
}

function updateHelpUI() {
    const helpContent = document.getElementById('helpContent');
    helpContent.innerHTML = `
        <div style="margin: 10px 0;">
            <h4>CONTROLS:</h4>
            <div>WASD or Arrow Keys: Move player</div>
            <div>Space: Interact with plants/soil</div>
            <div>E: Open shop</div>
            <div>Q: Open inventory</div>
            <div>H: Show this help</div>
            <div>ESC: Pause game or close menus</div>
        </div>
        <div style="margin: 20px 0;">
            <h4>GAMEPLAY:</h4>
            <div>• Plant seeds in soil tiles</div>
            <div>• Water plants regularly</div>
            <div>• Use fertilizer for better growth</div>
            <div>• Harvest mature plants for money</div>
            <div>• Buy upgrades in the shop</div>
            <div>• Expand your garden area</div>
        </div>
    `;
}

function purchaseItem(category, itemName) {
    if (game.purchaseItem(category, itemName)) {
        game.addNotification(`Purchased ${itemName}!`);
        updateUI();
    } else {
        game.addNotification("Not enough money!");
    }
}

function selectSeed(seedType) {
    game.player.selectSeed(seedType);
    updateUI();
}

function selectTool(toolName) {
    game.player.selectTool(toolName);
    updateUI();
}

// Game loop
function gameLoop(currentTime) {
    if (!running) return;
    
    const deltaTime = (currentTime - lastTime) / 1000.0;
    lastTime = currentTime;
    
    // Update game
    if (game.currentState === STATE_PLAYING) {
        game.update(deltaTime);
        game.updatePlayerMovement(deltaTime);
    }
    
    // Update UI
    updateUI();
    
    // Render
    renderer.clear();
    
    if (game.currentState === STATE_PAUSED) {
        renderer.renderPauseScreen();
    } else if (game.showShop) {
        renderer.renderShop(game.shop, game.economy);
    } else if (game.showInventory) {
        renderer.renderInventory(game.player);
    } else if (game.showHelp) {
        renderer.renderHelp();
    } else {
        // Render main game
        renderer.renderGarden(game.garden);
        
        // Render plants
        for (const plant of game.garden.plants.values()) {
            renderer.renderPlant(plant);
        }
        
        // Render player
        renderer.renderPlayer(game.player);
    }
    
    // Render notifications
    renderer.renderNotifications(game.notifications);
    
    // Continue loop
    requestAnimationFrame(gameLoop);
}

// Input handling
function handleKeyDown(event) {
    game.handleKeyDown(event.key);
}

function handleKeyUp(event) {
    game.handleKeyUp(event.key);
}

function handleMouseMove(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    game.handleMouseMove(x, y);
}

function handleMouseDown(event) {
    game.handleMouseDown(event.button);
}

function handleMouseUp(event) {
    game.handleMouseUp(event.button);
}

// Initialize game
function initGame() {
    // Get canvas
    canvas = document.getElementById('gameCanvas');
    
    // Create game and renderer
    game = new Game();
    renderer = new Renderer(canvas);
    
    // Set up event listeners
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mouseup', handleMouseUp);
    
    // Prevent context menu on right click
    canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    
    // Start game loop
    requestAnimationFrame(gameLoop);
}

// Start the game when page loads
window.addEventListener('load', initGame);
