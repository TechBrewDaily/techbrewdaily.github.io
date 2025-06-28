import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const publicDir = path.join(__dirname, 'public', 'images');

// Ensure directory exists
if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
}

// Generate SVG placeholder images
const generatePlaceholder = (width, height, text, filename) => {
    const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad${filename}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grad${filename})"/>
        <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">${text}</text>
    </svg>`;
    
    fs.writeFileSync(path.join(publicDir, `${filename}.svg`), svg);
    console.log(`Generated ${filename}.svg`);
};

// Generate placeholder images
generatePlaceholder(800, 400, 'TechBrew Daily', 'blog-placeholder-1');
generatePlaceholder(800, 400, 'Technology', 'blog-placeholder-2');
generatePlaceholder(800, 400, 'AI & Innovation', 'blog-placeholder-3');
generatePlaceholder(800, 400, 'Smart Tech', 'blog-placeholder-4');
generatePlaceholder(800, 400, 'Digital Trends', 'blog-placeholder-5');
generatePlaceholder(800, 400, 'Tech News', 'placeholder');
generatePlaceholder(1200, 630, 'TechBrew Daily', 'og-default');

console.log('All placeholder images generated successfully!');