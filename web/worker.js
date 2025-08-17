// Cloudflare Workers script for Grow Plants game
export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      const path = url.pathname;
      
      // Handle root path - serve index.html
      if (path === '/' || path === '') {
        const indexRequest = new Request(`${url.origin}/index.html`, request);
        return env.ASSETS.fetch(indexRequest);
      }
      
      // Try to serve the requested file
      try {
        const response = await env.ASSETS.fetch(request);
        
        // If file not found (404), serve index.html for SPA routing
        if (response.status === 404) {
          const indexRequest = new Request(`${url.origin}/index.html`, request);
          return env.ASSETS.fetch(indexRequest);
        }
        
        return response;
      } catch (fetchError) {
        // If fetch fails, serve index.html
        const indexRequest = new Request(`${url.origin}/index.html`, request);
        return env.ASSETS.fetch(indexRequest);
      }
      
    } catch (error) {
      // Ultimate fallback - return a simple error page
      return new Response('Game loading... Please refresh the page.', {
        status: 200,
        headers: {
          'Content-Type': 'text/plain',
          'Cache-Control': 'no-cache'
        }
      });
    }
  }
};
