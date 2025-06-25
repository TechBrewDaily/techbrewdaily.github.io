
import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  site: 'https://techbrewdaily.github.io',
  // IMPORTANT: The base must be '/' for an <org>.github.io repository
  base: '/',
  integrations: [
    tailwind({
      // This disables the default base styles from Astro's integration
      // so your own tailwind styles take full control.
      applyBaseStyles: false,
      }),
    ],
});