# File: autoblog_gemini.py

import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# --- CONFIG ---
AUTHOR = "TechBot"
BLOG_FOLDER = os.path.join("src", "content", "blog")

# --- SETUP ---
# Set Gemini API Key from environment variable
# Ensure you have GEMINI_API_KEY in your GitHub repository secrets
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
    return "The Future of Artificial Intelligence in India" # Fallback topic


def generate_blog_content(topic):
    """Asks Gemini to write ONLY the blog content, no frontmatter."""
    print(f"🧠 Generating blog content for topic: '{topic}'")
    
    # This prompt is specifically designed to get ONLY the article body.
    prompt = f"""
    Write a high-quality, SEO-optimized technical blog post for Indian readers on the topic: "{topic}"

    Instructions:
    1.  **ONLY write the article content.**
    2.  **DO NOT include the YAML frontmatter (the part with ---).**
    3.  Start directly with the first paragraph of the introduction.
    4.  Use clear H2 and H3 headings for structure.
    5.  Use bullet points for lists.
    6.  End with a short FAQ section if it makes sense for the topic.
    7.  The entire output must be valid Markdown.
    """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error generating content with Gemini: {e}")
        return ""


def save_markdown_file(title, content):
    """Creates a valid YAML frontmatter and combines it with the content."""
    if not content:
        print("No content was generated. Skipping file save.")
        return

    print("💾 Creating and saving blog file...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)

    today_for_filename = datetime.now().strftime("%Y%m%d")
    today_for_pubdate = datetime.now().strftime("%Y-%m-%d")
    
    # Create a safe description from the first 155 chars of content
    description = content.split('\n')[0].strip()[:155]

    # --- This is the key fix: We build the YAML ourselves ---
    # We replace any double quotes in the title to prevent breaking the YAML string.
    safe_title = title.replace('"', "'")
    safe_description = description.replace('"', "'")

    frontmatter = f"""---
title: "{safe_title}"
pubDate: "{today_for_pubdate}"
description: "{safe_description}"
author: "{AUTHOR}"
---

"""
    # ---------------------------------------------------------

    full_markdown = frontmatter + content
    filename = f"post-{today_for_filename}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_markdown)

    print(f"✅ Blog saved successfully at {filepath}")


def main():
    """Main function to run the autoblogger."""
    topic = fetch_trending_topic()
    blog_content = generate_blog_content(topic)
    save_markdown_file(topic, blog_content)


if __name__ == "__main__":
    main()