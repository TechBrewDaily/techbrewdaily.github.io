import { glob } from 'astro/loaders';
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
    // Load Markdown and MDX files in the `src/content/blog/` directory.
    loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
    // Type-check frontmatter using a schema
    schema: z.object({
        title: z.string(),
        description: z.string(),
        // Transform string to Date object
        pubDate: z.coerce.date(),
        updatedDate: z.coerce.date().optional(),
        author: z.string().optional(),
        // Make all fields optional with sensible defaults
        category: z.string().default('Technology'),
        tags: z.array(z.string()).default([]),
        image: z.object({
            url: z.string(),
            alt: z.string(),
        }).optional(),
        // Support both string and object formats for heroImage
        heroImage: z.union([
            z.string(), // Support legacy string format
            z.object({
                src: z.string(),
                width: z.number().optional(),
                height: z.number().optional(),
                format: z.union([
                    z.literal('png'), 
                    z.literal('jpg'), 
                    z.literal('jpeg'), 
                    z.literal('webp'), 
                    z.literal('avif'), 
                    z.literal('gif'), 
                    z.literal('svg')
                ]).optional(),
            })
        ]).optional(),
    }),
});

export const collections = { blog };
