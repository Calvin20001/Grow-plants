// Cloudflare Workers script for Grow Plants game
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // Default to index.html
    if (path === '/' || path === '') {
      return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
    }
    
    // Try to serve the requested file
    try {
      return await env.ASSETS.fetch(request);
    } catch (e) {
      // If file not found, return index.html for SPA routing
      return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
    }
  }
};
