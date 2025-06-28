import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import { defineCollection, z } from 'astro:content';

// https://astro.build/config
export default defineConfig({
  site: 'https://techbrewdaily.github.io',
  base: '/',
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
  ],
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

const blogCollection = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().optional(),
    category: z.string(),
    tags: z.array(z.string()),
    image: z.object({
      url: z.string(),
      alt: z.string(),
    }),
  }),
});

export const collections = {
  blog: blogCollection,
};