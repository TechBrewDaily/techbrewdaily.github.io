import google.generativeai as genai
from src.config import settings
from datetime import datetime
import json
import re
import random

def write_blog_post(topic: str, category_obj: dict) -> str | None:
    """Generates a full blog post with frontmatter (no image placeholders)."""
    print(f"✍️  Writing post for '{topic}'...")
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY_CONTENT)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Clean the topic for frontmatter
        clean_topic = topic.replace('"', "'").replace('\n', ' ').strip()
        
        # Create tags array properly for YAML
        tags = [category_obj['slug']] + category_obj['keywords'][:4]
        
        # Convert tags to proper YAML array format
        tags_yaml = "\n".join([f"  - \"{tag}\"" for tag in tags])
        
        # Get current date in ISO format (no quotes for date coercion)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Randomly select a placeholder image from available ones
        placeholder_images = [
            "/images/blog-placeholder-1.jpg",
            "/images/blog-placeholder-2.jpg", 
            "/images/blog-placeholder-3.jpg",
            "/images/blog-placeholder-4.jpg",
            "/images/blog-placeholder-5.jpg",
            "/images/placeholder.jpg"
        ]
        selected_image = random.choice(placeholder_images)
        
        prompt = f"""
        Write a high-quality tech blog post about: "{topic}"

        Write ONLY the content body (no frontmatter, no title heading):
        - Start with an engaging introduction paragraph
        - Use H2 (##) headings for main sections  
        - 800-1000 words total
        - Professional but approachable tone
        - Include practical tips and insights
        - End with a strong conclusion
        - Do NOT include any image placeholders or references
        - Do NOT start with a title heading
        - Do NOT include frontmatter

        Write the content starting immediately with the introduction paragraph.
        """
        
        response = model.generate_content(prompt)
        content_body = response.text.strip()
        
        # Remove any title headings that might have been generated
        lines = content_body.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.startswith('# '):
                print(f"🧹 Removing title heading: {line[:50]}...")
                continue
            cleaned_lines.append(line)
        
        content_body = '\n'.join(cleaned_lines)
        
        # Generate the complete markdown with proper frontmatter
        frontmatter = f"""---
title: "{clean_topic}"
description: "{clean_topic[:160]}"
pubDate: {current_date}
author: "{settings.AUTHOR}"
category: "{category_obj['name']}"
tags:
{tags_yaml}
image:
  url: "{selected_image}"
  alt: "Featured image for {clean_topic}"
---

{content_body}"""
        
        return frontmatter
        
    except Exception as e:
        print(f"❌ Error in Content Writer: {e}")
        return None