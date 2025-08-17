// Cloudflare Workers script for Grow Plants game
export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      const path = url.pathname;
      
      // Default to index.html for root path
      if (path === '/' || path === '') {
        return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
      }
      
      // Try to serve the requested file
      const response = await env.ASSETS.fetch(request);
      
      // If file not found, return index.html for SPA routing
      if (response.status === 404) {
        return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
      }
      
      return response;
    } catch (error) {
      // Fallback to index.html on any error
      return env.ASSETS.fetch(new Request(`${request.url.split('/')[0]}//${request.url.split('/')[2]}/index.html`, request));
    }
  }
};
