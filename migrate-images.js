import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const blogDir = path.join(__dirname, 'src', 'content', 'blog');

// Read all markdown files in the blog directory
fs.readdir(blogDir, (err, files) => {
    if (err) {
        console.error('Error reading blog directory:', err);
        return;
    }

    const markdownFiles = files.filter(file => file.endsWith('.md'));
    
    markdownFiles.forEach(file => {
        const filePath = path.join(blogDir, file);
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Replace .jpg references with .svg
        const updatedContent = content
            .replace(/\/images\/blog-placeholder-1\.jpg/g, '/images/blog-placeholder-1.svg')
            .replace(/\/images\/blog-placeholder-2\.jpg/g, '/images/blog-placeholder-2.svg')
            .replace(/\/images\/blog-placeholder-3\.jpg/g, '/images/blog-placeholder-3.svg')
            .replace(/\/images\/blog-placeholder-4\.jpg/g, '/images/blog-placeholder-4.svg')
            .replace(/\/images\/blog-placeholder-5\.jpg/g, '/images/blog-placeholder-5.svg')
            .replace(/\/images\/placeholder\.jpg/g, '/images/placeholder.svg');
        
        if (content !== updatedContent) {
            fs.writeFileSync(filePath, updatedContent);
            console.log(`✅ Updated ${file}`);
        }
    });
    
    console.log('🎉 Migration completed!');
});