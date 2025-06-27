import google.generativeai as genai
from src.config import settings
from datetime import datetime

def write_blog_post(topic: str, category_obj: dict) -> str | None:
    """Generates a full blog post with frontmatter and image placeholders."""
    print(f"✍️  Writing post for '{topic}'...")
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY_CONTENT)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a world-class tech blogger for "TechBrew Daily". Write a high-retention, SEO-optimized blog post on the topic: "{topic}".

        Follow these instructions precisely:
        1.  **Frontmatter:** Start with a valid YAML frontmatter block for Astro.
            - title: "{topic.replace('"', "'")}"
            - description: A compelling meta description under 160 characters.
            - pubDate: {datetime.now().strftime('%Y-%m-%d')}
            - author: "{settings.AUTHOR}"
            - category: "{category_obj['name']}"
            - tags: {str([category_obj['slug']] + category_obj['keywords'][:4])}
            - image:
                url: "[IMAGE_URL_PLACEHOLDER]"
                alt: "A descriptive alt text for the main hero image, related to '{topic.replace('"', "'")}'"
        2.  **Content:**
            - Write an engaging introduction.
            - Use at least 3-4 H2 (##) headings.
            - Total word count: 800-1000 words.
            - Tone: Knowledgeable, engaging, and slightly informal.
        3.  **Image Placeholders:** CRITICAL. Where a secondary picture would be effective (e.g., within 1-2 relevant sections), insert a placeholder in this exact format:
            `[IMAGE: A detailed, descriptive prompt for an AI image generator.]`
        4.  **Conclusion:** End with a strong summary.
        
        Respond with the complete markdown file content and nothing else.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error in Content Writer: {e}")
        return None