// astro.config.mjs
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import rss from '@astrojs/rss'; // Assuming you had this from the start

export default defineConfig({
  // Your GitHub repo name is 'astro-blog-techbrewdaily', not the final URL.
  // Set the `base` to the repo name. This is critical for GitHub Pages.
  site: 'https://jainhardik06.github.io',
  base: '/astro-blog-techbrewdaily/', 
  
  integrations: [mdx(), sitemap(), rss()],
  // Notice: The 'adapter' line is completely removed.
});