import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# CONFIG
AUTHOR = "TechBot"
BLOG_FOLDER = os.path.join("src", "content", "blog")

# Set Gemini API Key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def fetch_trending_topic():
    print("🔍 Fetching trending topic from Google News...")
    feed = feedparser.parse("https://news.google.com/rss/search?q=technology+india&hl=en-IN&gl=IN&ceid=IN:en")
    return feed.entries[0].title if feed.entries else "Latest Tech News in India"

def generate_blog_content(topic):
    print("🧠 Generating blog content with Gemini...")
    prompt = f"""
Write a detailed technical blog for Indian readers on the topic:
"{topic}"

Only return the content of the blog. Do NOT include YAML frontmatter.
Include:
- 2-line intro
- H2 and H3 headings
- Bullet points if needed
- A short FAQ at the end if applicable
Use valid markdown. No YAML, no triple backticks, no metadata.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def create_yaml_frontmatter(title, date, description, author):
    # Ensure quotes are added properly around values
    frontmatter = f"""---
title: "{title.replace('"', "'")}"
pubDate: "{date}"
description: "{description.replace('"', "'")}"
author: "{author}"
---\n
"""
    return frontmatter

def save_markdown(title, blog_content):
    print("💾 Saving blog file...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"post-{today}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)

    # Create frontmatter
    description = blog_content.split("\n")[0][:150]  # First line as meta description
    yaml = create_yaml_frontmatter(title, date_str, description, AUTHOR)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(yaml + blog_content)

    print(f"✅ Blog saved at {filepath}")
    return filepath

def main():
    title = fetch_trending_topic()
    content = generate_blog_content(title)
    save_markdown(title, content)

if __name__ == "__main__":
    main()
