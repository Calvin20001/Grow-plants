# 🌱 Grow Plants - Web Version

A complete web-based version of the Grow Plants game that can be deployed to Cloudflare Workers!

## 🚀 **Deploy to Cloudflare Workers**

### Prerequisites
- [Cloudflare account](https://dash.cloudflare.com/sign-up)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed

### Quick Deploy

1. **Install Wrangler CLI:**
   ```bash
   npm install -g wrangler
   ```

2. **Login to Cloudflare:**
   ```bash
   wrangler login
   ```

3. **Deploy the game:**
   ```bash
   cd web
   wrangler deploy
   ```

4. **Your game will be available at:**
   ```
   https://grow-plants-game.your-subdomain.workers.dev
   ```

## 🎮 **How to Play**

### Controls
- **WASD/Arrow Keys**: Move player
- **Space**: Interact with plants/soil
- **E**: Open shop
- **Q**: Open inventory  
- **H**: Show help
- **ESC**: Pause/Close menus

### Gameplay
1. **Plant seeds** in soil tiles
2. **Water plants** regularly for optimal growth
3. **Use fertilizer** to boost growth and mutation chances
4. **Harvest mature plants** for money
5. **Buy upgrades** in the shop
6. **Expand your garden** area

## 🌟 **Features**

- **Complete plant growth system** with 5 stages
- **Mutation system** for rare, valuable plants
- **Dynamic economy** with market fluctuations
- **Weather system** affecting plant growth
- **Shop system** with progression unlocks
- **Player progression** with experience and leveling
- **Responsive web interface** that works on all devices

## 🏗️ **Architecture**

- **Frontend**: HTML5 Canvas + JavaScript
- **Backend**: Cloudflare Workers (static file serving)
- **Game Engine**: Custom JavaScript game loop
- **Graphics**: Canvas 2D rendering
- **Input**: Keyboard and mouse handling

## 📁 **File Structure**

```
web/
├── index.html          # Main game page
├── js/
│   ├── constants.js    # Game configuration
│   ├── plant.js        # Plant class
│   ├── garden.js       # Garden management
│   ├── player.js       # Player character
│   ├── economy.js      # Economic system
│   ├── shop.js         # Shop system
│   ├── game.js         # Main game logic
│   ├── renderer.js     # Graphics rendering
│   └── main.js         # Game initialization
├── wrangler.toml       # Cloudflare Workers config
├── worker.js           # Workers script
└── README.md           # This file
```

## 🔧 **Customization**

### Adding New Plants
Edit `js/constants.js` to add new plant types:

```javascript
const PLANT_TYPES = {
    "carrot": { /* existing */ },
    "new_plant": {
        name: "New Plant",
        growth_time: 10.0,
        water_need: 3,
        base_value: 30,
        mutation_chance: 0.05,
        color: COLORS.PURPLE
    }
};
```

### Modifying Game Balance
Adjust values in `js/constants.js`:
- `STARTING_MONEY`: Starting currency
- `BASE_GROWTH_TIME`: Base plant growth speed
- `MUTATION_CHANCE`: Base mutation probability

## 🌐 **Browser Compatibility**

- **Modern browsers**: Chrome, Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile
- **Requires**: JavaScript enabled, Canvas support

## 📱 **Mobile Support**

The game automatically adapts to mobile devices:
- Touch-friendly controls
- Responsive canvas sizing
- Mobile-optimized UI

## 🚀 **Performance**

- **60 FPS** game loop
- **Efficient rendering** with Canvas 2D
- **Minimal memory usage**
- **Fast loading** with Cloudflare's global CDN

## 🔒 **Security**

- **No server-side game logic** (client-side only)
- **Static file serving** via Cloudflare Workers
- **No user data collection**
- **Open source** and transparent

## 🆘 **Troubleshooting**

### Game won't load
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled
- Try refreshing the page

### Performance issues
- Close other browser tabs
- Check if hardware acceleration is enabled
- Try a different browser

### Deployment issues
- Verify Wrangler CLI is installed and logged in
- Check Cloudflare account status
- Review Workers deployment logs

## 📞 **Support**

If you encounter issues:
1. Check the browser console for error messages
2. Verify all files are properly deployed
3. Test with a different browser
4. Check Cloudflare Workers status

## 🎉 **Enjoy Your Garden!**

The web version provides the same engaging gameplay as the desktop version, but now you can play from anywhere with a web browser! Share your garden empire with friends and family by simply sharing the URL.

---

**Happy Gardening! 🌱💰**
