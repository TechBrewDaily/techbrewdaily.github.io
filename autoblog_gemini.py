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
    print(f"✍️  Generating metadata for topic: '{topic}'")
    
    # Prompt for generating only metadata in JSON format
    prompt = f"""
    Based on the following topic, generate a catchy, SEO-friendly blog post title and a meta description.
    
    Topic: "{topic}"
    
    Instructions:
    - The title should be engaging and under 70 characters.
    - The description should be a concise summary under 160 characters.
    - Provide the output ONLY in a valid JSON format like this:
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
        # Return a safe fallback
        return topic, "A summary of the latest in Indian technology."

def generate_blog_content(topic):
    """Asks Gemini to write ONLY the blog article content."""
    print(f"🧠 Generating blog content for topic: '{topic}'")
    
    prompt = f"""
    Write a high-quality, SEO-optimized technical blog post for Indian readers on the topic: "{topic}"

    Instructions:
    1.  **ONLY write the article content.**
    2.  **DO NOT include the YAML frontmatter (the part with ---).**
    3.  Start directly with the first paragraph of the introduction.
    4.  Use clear H2 and H3 headings for structure.
    5.  Use bullet points for lists.
    6.  The entire output must be valid Markdown.
    """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error generating blog content: {e}")
        return ""

def save_markdown_file(title, description, content):
    """Creates a valid YAML frontmatter and combines it with the content."""
    if not content:
        print("No content was generated. Skipping file save.")
        return

    print("💾 Creating and saving blog file...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)

    today_for_filename = datetime.now().strftime("%Y%m%d")
    today_for_pubdate = datetime.now().strftime("%Y-%m-%d")
    
    # Sanitize inputs for YAML safety
    safe_title = title.replace('"', "'")
    safe_description = description.replace('"', "'")

    frontmatter = f"""---
title: "{safe_title}"
pubDate: "{today_for_pubdate}"
description: "{safe_description}"
author: "{AUTHOR}"
---

"""

    full_markdown = frontmatter + content
    filename = f"post-{today_for_filename}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_markdown)

    print(f"✅ Blog saved successfully at {filepath}")

def main():
    """Main function to run the autoblogger."""
    raw_topic = fetch_trending_topic()
    title, description = generate_metadata(raw_topic)
    blog_content = generate_blog_content(title) # Use the new, better title for the content
    save_markdown_file(title, description, blog_content)

if __name__ == "__main__":
    main()