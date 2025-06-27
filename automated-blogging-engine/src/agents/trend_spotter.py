import google.generativeai as genai
from src.config import settings

def find_trending_topic(category_obj: dict, used_topics: set) -> str | None:
    """Finds a fresh, SEO-friendly topic for a given category."""
    category_name = category_obj['name']
    print(f"🕵️  Finding topic for '{category_name}'...")
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY_TOPICS)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert SEO strategist for a tech blog, "TechBrew Daily".
        Generate ONE compelling, long-tail keyword blog post title for the category: "{category_name}".
        The title must be fresh, specific, and something users are actively searching for.
        AVOID generic topics.
        Most importantly, DO NOT use any of these previously used titles: {', '.join(used_topics)}.
        Respond with ONLY the blog post title.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip().replace('"', '')
    except Exception as e:
        print(f"❌ Error in Trend Spotter: {e}")
        return None