// astro.config.mjs
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import rss, { pagesGlobToRssItems } from '@astrojs/rss';

export default defineConfig({
  site: 'https://jainhardik06.github.io',
  base: '/astro-blog-techbrewdaily/',

  integrations: [
    mdx(),
    sitemap(),
    rss({
      title: 'Tech Brew Daily Blog',
      description: 'A daily dose of tech news and insights.',
      items: pagesGlobToRssItems(
        import.meta.glob('./src/content/blog/**/*.{md,mdx}')
      ),
      customData: `<language>en-us</language>`,
    }),
  ],
});