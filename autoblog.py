# File: autoblog.py

import openai
import os
import feedparser
from datetime import datetime

# --- CONFIGURATION ---
AUTHOR_NAME = "TechBot"
BLOG_REPO_DIR = os.path.dirname(os.path.abspath(__file__))  # assumes script is in repo root
BLOG_FOLDER = os.path.join(BLOG_REPO_DIR, "src", "content", "blog")

# Read OpenAI API Key from environment (set in GitHub Actions)
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_trending_topic():
    """
    Fetches the top trending Indian tech headline from Google News RSS.
    """
    print("🔍 Fetching trending topic from Google News...")
    feed_url = "https://news.google.com/rss/search?q=technology+india&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return "Latest Tech Update in India"

    topic = feed.entries[0].title
    print(f"📰 Topic found: {topic}")
    return topic


def generate_blog_from_topic(topic):
    """
    Uses OpenAI to generate a markdown blog post for the topic.
    """
    print("🤖 Generating blog content with OpenAI...")
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
    Write a detailed, SEO-optimized tech blog post in markdown about "{topic}" for Indian readers.

    Format:
    ---
    title: "Catchy SEO Title"
    pubDate: "{today}"
    description: "A short summary under 160 characters."
    author: "{AUTHOR_NAME}"
    ---

    Use Markdown. Include:
    - A 2-line intro
    - H2 and H3 headings
    - Bullet points
    - A short FAQ section at the end if relevant
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def save_markdown_file(markdown):
    """
    Saves the markdown content to the Astro blog folder.
    """
    print("📁 Saving markdown file...")
    try:
        title_line = next(line for line in markdown.splitlines() if line.startswith("title:"))
        title = title_line.split(":", 1)[1].strip().strip('"')
        filename = title.lower().replace(" ", "-")[:40] + ".md"
    except:
        filename = f"post-{datetime.now().strftime('%Y%m%d')}.md"

    os.makedirs(BLOG_FOLDER, exist_ok=True)
    filepath = os.path.join(BLOG_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Blog post saved to: {filepath}")
    return filename


def main():
    topic = fetch_trending_topic()
    markdown = generate_blog_from_topic(topic)
    save_markdown_file(markdown)


if __name__ == "__main__":
    main()
