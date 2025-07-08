import google.generativeai as genai
from src.config import settings
from datetime import datetime
import json
import re
import random

def generate_seo_title_and_meta(topic: str, category_obj: dict) -> tuple[str, str]:
    """Generate SEO-optimized title and meta description."""
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY_CONTENT)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Create an SEO-optimized title and meta description for a tech blog post about: "{topic}"
        Category: {category_obj['name']}
        Keywords: {', '.join(category_obj['keywords'][:3])}

        Requirements for TITLE:
        - 50-60 characters maximum
        - Include primary keyword from topic
        - Be compelling and clickable
        - Include current year (2025) if relevant
        - Use power words like "Complete Guide", "Ultimate", "Best", "How to", "Top"
        - Avoid clickbait, be accurate

        Requirements for META DESCRIPTION:
        - 150-160 characters maximum
        - Include primary and secondary keywords
        - Include a clear benefit/value proposition
        - End with a call to action
        - Be compelling but accurate

        Return ONLY valid JSON:
        {{"title": "Your SEO Title Here", "description": "Your meta description here."}}
        """
        
        response = model.generate_content(prompt)
        cleaned_json = response.text.strip().replace("```json", "").replace("```", "")
        
        try:
            metadata = json.loads(cleaned_json)
            return metadata['title'], metadata['description']
        except:
            # Fallback to improved basic title
            fallback_title = f"Complete Guide to {topic} in 2025"[:60]
            fallback_desc = f"Discover everything about {topic}. Expert insights, practical tips, and latest trends in {category_obj['name'].lower()}."[:160]
            return fallback_title, fallback_desc
            
    except Exception as e:
        print(f"❌ Error generating SEO metadata: {e}")
        fallback_title = f"Complete Guide to {topic} in 2025"[:60]
        fallback_desc = f"Discover everything about {topic}. Expert insights and practical tips."[:160]
        return fallback_title, fallback_desc

def write_blog_post(topic: str, category_obj: dict) -> str | None:
    """Generates a full blog post with frontmatter (with proper image paths)."""
    print(f"✍️  Writing SEO-optimized post for '{topic}'...")
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY_CONTENT)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate SEO-optimized title and description
        seo_title, seo_description = generate_seo_title_and_meta(topic, category_obj)
        print(f"📝 Generated SEO title: {seo_title}")
        
        # Clean the title for frontmatter
        clean_title = seo_title.replace('"', "'").replace('\n', ' ').strip()
        clean_description = seo_description.replace('"', "'").replace('\n', ' ').strip()
        
        # Create tags array properly for YAML
        tags = [category_obj['slug']] + category_obj['keywords'][:4]
        
        # Convert tags to proper YAML array format
        tags_yaml = "\n".join([f"  - \"{tag}\"" for tag in tags])
        
        # Get current date in ISO format (no quotes for date coercion)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # FIX: Use .svg placeholders (matching what we actually generated)
        placeholder_images = [
            "/images/blog-placeholder-1.svg",
            "/images/blog-placeholder-2.svg", 
            "/images/blog-placeholder-3.svg",
            "/images/blog-placeholder-4.svg",
            "/images/blog-placeholder-5.svg",
            "/images/placeholder.svg"
        ]
        selected_image = random.choice(placeholder_images)
        
        # Enhanced SEO-focused content prompt
        prompt = f"""
        Write a comprehensive, SEO-optimized tech blog post about: "{topic}"
        Target title: "{seo_title}"
        Category: {category_obj['name']}
        Target keywords: {', '.join(category_obj['keywords'][:5])}

        SEO REQUIREMENTS:
        - Write 1200-1500 words for better SEO ranking
        - Include target keywords naturally (keyword density 1-2%)
        - Use semantic keywords and related terms
        - Include the year 2025 where relevant
        - Structure with proper H2 and H3 headings
        - Include numbered lists and bullet points
        - Add a clear conclusion with actionable takeaways

        CONTENT STRUCTURE:
        1. Start with an engaging hook (2-3 sentences)
        2. Introduction paragraph explaining what readers will learn
        3. ## Main sections (4-6 H2 headings)
        4. Use ### subsections where appropriate
        5. Include "## Frequently Asked Questions" section with 3-4 Q&As
        6. End with "## Conclusion" and clear takeaways

        WRITING STYLE:
        - Professional but accessible tone
        - Use active voice
        - Include practical examples and real-world applications
        - Add specific statistics or trends (use realistic but general claims)
        - Avoid fluff and filler content
        - Each paragraph should provide value
        - Use transition words for better readability

        IMPORTANT RESTRICTIONS:
        - Do NOT include any frontmatter or YAML
        - Do NOT include the main title as an H1
        - Start directly with the introduction paragraph
        - Do NOT include any image references or placeholders
        - Keep paragraphs between 2-4 sentences
        - Use simple, clear language

        Begin writing the content immediately:
        """
        
        response = model.generate_content(prompt)
        content_body = response.text.strip()
        
        # Remove any title headings that might have been generated
        lines = content_body.split('\n')
        cleaned_lines = []
        skip_next_empty = False
        
        for i, line in enumerate(lines):
            # Remove any H1 titles or main title references
            if line.startswith('# ') or (line.strip() and seo_title.lower() in line.lower() and i < 5):
                print(f"🧹 Removing title heading: {line[:50]}...")
                skip_next_empty = True
                continue
            # Skip empty lines immediately after removed titles
            if skip_next_empty and line.strip() == "":
                skip_next_empty = False
                continue
            skip_next_empty = False
            cleaned_lines.append(line)
        
        content_body = '\n'.join(cleaned_lines).strip()
        
        # Generate the complete markdown with proper frontmatter
        frontmatter = f"""---
title: "{clean_title}"
description: "{clean_description}"
pubDate: {current_date}
author: "{settings.AUTHOR}"
category: "{category_obj['name']}"
tags:
{tags_yaml}
image:
  url: "{selected_image}"
  alt: "Featured image for {clean_title}"
---

{content_body}"""
        
        return frontmatter
        
    except Exception as e:
        print(f"❌ Error in Content Writer: {e}")
        return None