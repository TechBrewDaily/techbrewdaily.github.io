import google.generativeai as genai
import uuid
import os
import time
from src.config import settings

def generate_and_save_image(prompt: str, post_slug: str) -> str | None:
    """Generates an image from a prompt and saves it locally."""
    print(f"🎨 Generating image for: '{prompt[:50]}...'")
    
    if not settings.GEMINI_API_KEY_IMAGES:
        print("⚠️ Image generation skipped: API key not configured.")
        return None

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY_IMAGES)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        full_prompt = f"Generate a high-quality, 16:9 aspect ratio, vibrant blog post image. Do not include text. Prompt: {prompt}"
        
        response = model.generate_content([full_prompt])
        
        image_data = response.parts[0].blob.data

        unique_id = str(uuid.uuid4())[:8]
        image_filename = f"{post_slug}-{unique_id}.png"
        
        os.makedirs(settings.IMAGE_SAVE_PATH, exist_ok=True)
        
        image_filepath = os.path.join(settings.IMAGE_SAVE_PATH, image_filename)
        with open(image_filepath, "wb") as f:
            f.write(image_data)
        
        print(f"✅ Image saved: {image_filepath}")
        
        return os.path.join(settings.IMAGE_PUBLIC_PATH, image_filename).replace("\\", "/")

    except Exception as e:
        print(f"❌ Failed to generate or save image: {e}")
        return None
    finally:
        # FIX: Increase delay to 35 seconds to safely stay within the
        # free tier limit for the gemini-1.5-pro model (e.g., 2 RPM).
        wait_time = 35
        print(f"⏳ Waiting for {wait_time} seconds to avoid rate limits...")
        time.sleep(wait_time)