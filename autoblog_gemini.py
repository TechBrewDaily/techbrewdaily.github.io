# File: autoblog_gemini.py

import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# CONFIGURATION
AUTHOR = "AutoBlog Bot"
BLOG_FOLDER = os.path.join("src", "content", "blog")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def fetch_trending_topic():
    print("🔍 Fetching trending topic from Google News...")
    feed = feedparser.parse("https://news.google.com/rss/search?q=technology+india&hl=en-IN&gl=IN&ceid=IN:en")
    return feed.entries[0].title if feed.entries else "Latest Tech News in India"

def generate_blog(topic):
    print("🧠 Generating blog using Gemini...")

    # Initialize the model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    # Prompt WITHOUT frontmatter
    prompt = f"""
Write a detailed SEO-optimized technical blog article in Markdown format (no frontmatter, just pure content) on the topic:
"{topic}"

Instructions:
- Start with a 2-line intro
- Use H2 and H3 headings appropriately
- Include bullet points where relevant
- End with a short FAQ section
- Use proper Markdown formatting
- Keep the tone professional and relevant to Indian tech readers
- Do not add YAML frontmatter or metadata like title/date/author
"""

    response = model.generate_content(prompt)
    markdown_body = response.text.strip()

    # Generate metadata (frontmatter)
    today = datetime.now().strftime("%Y-%m-%d")
    frontmatter = f"""---
title: "{topic.replace('"', "'")}"
pubDate: "{today}"
description: "Auto-generated blog on '{topic}' for Indian tech readers."
author: "{AUTHOR}"
---

"""

    return frontmatter + markdown_body

def save_markdown(markdown):
    print("💾 Saving blog post...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filename = f"post-{today}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Blog saved at: {filepath}")
    return filepath

def main():
    topic = fetch_trending_topic()
    markdown = generate_blog(topic)
    save_markdown(markdown)

if __name__ == "__main__":
    main()
