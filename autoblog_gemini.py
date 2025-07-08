# File: autoblog_gemini.py

import os
import google.generativeai as genai
import feedparser
from datetime import datetime
import json

# --- CONFIG ---
AUTHOR = "TechBot"
BLOG_FOLDER = os.path.join("src", "content", "blog")

# --- SETUP ---
# Configure the Gemini API Key
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    exit(1)

def fetch_trending_topic():
    """Fetches the latest tech news title from Google News India."""
    print("🔍 Fetching trending topic from Google News...")
    feed = feedparser.parse("https://news.google.com/rss/search?q=technology+india&hl=en-IN&gl=IN&ceid=IN:en")
    if feed.entries:
        return feed.entries[0].title
    return "The Future of Artificial Intelligence in India"  # Fallback topic

def generate_metadata(topic):
    """Generates a catchy SEO title and a meta description."""
    print(f"✍️  Generating SEO metadata for topic: '{topic}'")
    
    # Prompt for generating only metadata in JSON format
    prompt = f"""
    Based on the following topic, generate a highly SEO-optimized blog post title and meta description.
    
    Topic: "{topic}"
    
    Requirements for TITLE:
    - 50-60 characters maximum
    - Include primary keyword from topic
    - Be compelling and clickable for Indian tech audience
    - Include current year (2025) if relevant
    - Use power words like "Complete Guide", "Ultimate", "Best", "How to", "Top", "Latest"
    - Avoid clickbait, be accurate and professional
    - Focus on value proposition

    Requirements for META DESCRIPTION:
    - 150-160 characters maximum
    - Include primary and secondary keywords naturally
    - Include a clear benefit/value proposition
    - Mention "India" or "Indian" if relevant to topic
    - End with engaging call to action
    - Be compelling but accurate

    Examples of good titles:
    - "Complete Guide to AI in India 2025: Trends & Opportunities"
    - "Top 10 Fintech Innovations Transforming Indian Banking"
    - "How to Build Your Tech Startup in India: Ultimate Guide"

    Provide the output ONLY in a valid JSON format like this:
    {{"title": "Your SEO-Friendly Title", "description": "Your meta description here."}}
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        cleaned_json = response.text.strip().replace("```json", "").replace("```", "")
        metadata = json.loads(cleaned_json)
        return metadata['title'], metadata['description']
    except Exception as e:
        print(f"❌ Error generating or parsing metadata: {e}")
        # Return improved SEO fallback
        fallback_title = f"Complete Guide to {topic} in India 2025"[:60]
        fallback_desc = f"Discover everything about {topic} in India. Expert insights, latest trends, and practical tips for tech enthusiasts."[:160]
        return fallback_title, fallback_desc

def generate_blog_content(topic, seo_title):
    """Asks Gemini to write ONLY the blog article content."""
    print(f"🧠 Generating SEO-optimized blog content for: '{seo_title}'")
    
    prompt = f"""
    Write a comprehensive, SEO-optimized technical blog post for Indian readers.
    
    Original Topic: "{topic}"
    SEO Title: "{seo_title}"
    Target Audience: Indian tech enthusiasts, professionals, and beginners
    
    SEO REQUIREMENTS:
    - Write 1200-1500 words for better search ranking
    - Include target keywords naturally throughout (keyword density 1-2%)
    - Use semantic keywords and related technical terms
    - Include the year 2025 where relevant
    - Structure with proper H2 and H3 headings for better readability
    - Include numbered lists and bullet points
    - Add a comprehensive FAQ section with 4-5 questions
    - Include practical examples relevant to Indian market
    
    CONTENT STRUCTURE:
    1. Start with an engaging hook and clear value proposition (2-3 sentences)
    2. Introduction paragraph explaining what readers will learn
    3. 4-6 main sections with H2 headings (##)
    4. Use H3 subsections (###) where appropriate
    5. Include "## Frequently Asked Questions" section with detailed Q&As
    6. End with "## Conclusion" and clear, actionable takeaways
    
    WRITING STYLE:
    - Professional but accessible tone for Indian audience
    - Use active voice and clear, simple language
    - Include practical examples and real-world applications in Indian context
    - Add specific, realistic statistics and trends
    - Avoid fluff and filler content - every paragraph must provide value
    - Use transition words for better readability
    - Keep paragraphs between 2-4 sentences
    - Include references to Indian companies, startups, or examples where relevant
    
    IMPORTANT RESTRICTIONS:
    - **DO NOT include the YAML frontmatter (the part with ---).**
    - **DO NOT include the main title as an H1 heading.**
    - Start directly with the first paragraph of the introduction.
    - **DO NOT include any image references or placeholders.**
    - Use clear H2 and H3 headings for structure.
    - Use bullet points and numbered lists for better readability.
    - The entire output must be valid Markdown.
    - Focus on providing genuine value and accurate information.
    
    Begin writing the content immediately with the introduction paragraph:
    """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Remove any accidentally generated title headings
        lines = content.split('\n')
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
        
        return '\n'.join(cleaned_lines).strip()
    except Exception as e:
        print(f"❌ Error generating blog content: {e}")
        return ""

def save_markdown_file(title, description, content):
    """Creates a valid YAML frontmatter and combines it with the content."""
    if not content:
        print("No content was generated. Skipping file save.")
        return

    print("💾 Creating and saving SEO-optimized blog file...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)

    today_for_filename = datetime.now().strftime("%Y%m%d")
    today_for_pubdate = datetime.now().strftime("%Y-%m-%d")
    
    # Sanitize inputs for YAML safety
    safe_title = title.replace('"', "'")
    safe_description = description.replace('"', "'")

    # Generate SEO-friendly tags
    tags = ["technology", "india", "tech-news", "innovation"]
    
    # Add specific tags based on title content
    title_lower = title.lower()
    if "ai" in title_lower or "artificial intelligence" in title_lower:
        tags.extend(["ai", "artificial-intelligence", "machine-learning"])
    if "startup" in title_lower:
        tags.extend(["startup", "entrepreneurship", "business"])
    if "fintech" in title_lower:
        tags.extend(["fintech", "finance", "banking"])
    if "mobile" in title_lower or "app" in title_lower:
        tags.extend(["mobile-apps", "android", "ios"])
    if "blockchain" in title_lower or "crypto" in title_lower:
        tags.extend(["blockchain", "cryptocurrency", "web3"])
    
    # Remove duplicates and limit to 8 tags
    tags = list(dict.fromkeys(tags))[:8]
    tags_yaml = "\n".join([f"  - \"{tag}\"" for tag in tags])

    frontmatter = f"""---
title: "{safe_title}"
pubDate: "{today_for_pubdate}"
description: "{safe_description}"
author: "{AUTHOR}"
category: "Technology"
tags:
{tags_yaml}
image:
  url: "/images/blog-placeholder-1.svg"
  alt: "Featured image for {safe_title}"
---

"""

    full_markdown = frontmatter + content
    filename = f"post-{today_for_filename}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_markdown)

    print(f"✅ SEO-optimized blog saved successfully at {filepath}")
    print(f"📝 Title: {title}")
    print(f"📊 Word count: approximately {len(content.split())} words")

def main():
    """Main function to run the SEO-optimized autoblogger."""
    print("🚀 Starting SEO-Optimized TechBrew Daily Auto-Blogger...")
    
    raw_topic = fetch_trending_topic()
    title, description = generate_metadata(raw_topic)
    blog_content = generate_blog_content(raw_topic, title) # Use both original topic and SEO title
    save_markdown_file(title, description, blog_content)
    
    print("✅ SEO-optimized blog generation complete!")

if __name__ == "__main__":
    main()