import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string().optional(),
    heroImage: z.string().optional(),
    // For a professional look, we need a featured image.
    image: z.object({
      url: z.string(),
      alt: z.string()
    }).optional(), // Optional so old posts don't break
  }),
});

export const collections = {
  'blog': blogCollection,
};