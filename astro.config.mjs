// astro.config.mjs
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
// The 'rss' import has been removed.

export default defineConfig({
  site: 'https://jainhardik06.github.io',
  base: '/astro-blog-techbrewdaily/',

  integrations: [
    mdx(),
    sitemap(),
    // The entire rss({...}) block has been removed.
  ],
});