import google.generativeai as genai
import uuid
import os
import time
from src.config import settings

def generate_and_save_image(prompt: str, post_slug: str) -> str | None:
    """Placeholder function - image generation disabled."""
    print(f"🖼️ Image generation disabled for: '{prompt[:50]}...'")
    return None