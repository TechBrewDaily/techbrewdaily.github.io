# File: autoblog_gemini.py

import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# CONFIG
AUTHOR = "TechBot"
BLOG_FOLDER = os.path.join("src", "content", "blog")  # for Astro blog

# Set your Gemini API Key (OR use environment variable later)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def fetch_trending_topic():
    print("🔍 Fetching trending topic from Google News...")
    feed = feedparser.parse("https://news.google.com/rss/search?q=technology+india&hl=en-IN&gl=IN&ceid=IN:en")
    return feed.entries[0].title if feed.entries else "Latest Tech News in India"


def generate_blog(topic):
    print("🧠 Generating blog with Gemini...")
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
    Write a detailed SEO-optimized technical blog in markdown format for Indian readers on the topic:
    "{topic}"

    Format:
    ---
    title: "SEO-friendly title"
    pubDate: "{today}"
    description: "Short summary under 160 characters"
    author: "{AUTHOR}"
    ---

    Content:
    - 2-line intro
    - H2 and H3 headings
    - Bullet points
    - Short FAQ at the end (if relevant)
    - Use Markdown
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


def save_markdown(markdown):
    print("💾 Saving blog file...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filename = f"post-{today}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Blog saved at {filepath}")
    return filepath


def main():
    topic = fetch_trending_topic()
    blog = generate_blog(topic)
    save_markdown(blog)


if __name__ == "__main__":
    main()
