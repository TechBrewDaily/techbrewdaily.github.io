import os
import re
from src.config import settings

def generate_slug(topic: str) -> str:
    """Creates a URL-friendly slug from a topic string."""
    slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')[:60]
    return slug

def save_markdown_file(content: str, slug: str):
    """Saves the final markdown content to a file using a pre-generated slug."""
    try:
        # FIX: Ensure the directory exists before trying to write the file
        os.makedirs(settings.POSTS_PATH, exist_ok=True)
        
        filepath = os.path.join(settings.POSTS_PATH, f"{slug}.md")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Successfully created/updated post: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return False