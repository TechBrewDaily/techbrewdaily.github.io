// astro.config.mjs
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import rss from '@astrojs/rss';

export default defineConfig({
  // These must be correct for the RSS feed links to work properly
  site: 'https://jainhardik06.github.io',
  base: '/astro-blog-techbrewdaily/',

  integrations: [
    mdx(),
    sitemap(),
    
    // HERE IS THE FIX:
    // The rss() integration needs a configuration object.
    rss({
      // (Required) The title for your RSS feed.
      title: 'Tech Brew Daily Blog',
      // (Required) A description for your RSS feed.
      description: 'A daily dose of tech news and insights.',
      // This points to the blog posts that should be in the feed.
      // This assumes your posts are in `src/content/blog/`
      items: import.meta.glob('./src/content/blog/**/*.mdx'),
      // (Optional)
      customData: `<language>en-us</language>`,
    }),
  ],
});