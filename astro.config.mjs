import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  site: 'https://jainhardik06.github.io',
  base: '/astro-blog-techbrewdaily',
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
  ],
  // Optimize for static deployment
  output: 'static',
  // Add image optimization
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
  },
  // Ensure proper static file handling
  vite: {
    assetsInclude: ['**/*.jpg', '**/*.jpeg', '**/*.png', '**/*.gif', '**/*.svg', '**/*.webp']
  }
});