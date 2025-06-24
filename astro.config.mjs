// astro.config.mjs
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://jainhardik06.github.io',
  base: '/astro-blog-techbrewdaily/',
  integrations: [mdx(), sitemap()],
});
