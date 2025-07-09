import { getCollection } from 'astro:content';

export async function GET() {
  const posts = await getCollection('blog');
  const lastMod = new Date().toISOString();
  
  // Generate additional sitemap content
  const additionalUrls = [
    { url: 'https://techbrewdaily.github.io/', priority: '1.0', changefreq: 'daily' },
    { url: 'https://techbrewdaily.github.io/blog/', priority: '0.9', changefreq: 'daily' },
    { url: 'https://techbrewdaily.github.io/about/', priority: '0.8', changefreq: 'weekly' },
  ];

  // Add category pages
  const categories = ['technology', 'ai', 'startups', 'programming', 'reviews'];
  categories.forEach(cat => {
    additionalUrls.push({
      url: `https://techbrewdaily.github.io/category/${cat}/`,
      priority: '0.7',
      changefreq: 'weekly'
    });
  });

  // Add all blog posts
  posts.forEach(post => {
    additionalUrls.push({
      url: `https://techbrewdaily.github.io/blog/${post.slug}/`,
      priority: '0.6',
      changefreq: 'monthly'
    });
  });

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
${additionalUrls.map(({ url, priority, changefreq }) => `  <url>
    <loc>${url}</loc>
    <lastmod>${lastMod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'max-age=3600'
    }
  });
}
