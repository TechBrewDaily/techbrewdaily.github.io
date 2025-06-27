import os
from dotenv import load_dotenv

# Load environment variables from a .env file in the project root
load_dotenv()

# --- API KEYS ---
GEMINI_API_KEY_TOPICS = os.getenv("GEMINI_API_KEY_1")
GEMINI_API_KEY_CONTENT = os.getenv("GEMINI_API_KEY_2")
GEMINI_API_KEY_IMAGES = os.getenv("GEMINI_API_KEY_3")

# --- PATHS ---
# Use an environment variable for the path in production (GitHub Actions),
# with a fallback to the local relative path for development.
ASTRO_PROJECT_ROOT_NAME = 'astro-blog-techbrewdaily'
# In GitHub Actions, GITHUB_WORKSPACE will be the root d:\astro-blog-techbrewdaily
# Locally, we find the parent directory of the current script's project.
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ASTRO_PROJECT_PATH = os.path.join(
    os.getenv('GITHUB_WORKSPACE', os.path.dirname(_project_root)), 
    ASTRO_PROJECT_ROOT_NAME
)

# Paths within the Astro project
POSTS_PATH = os.path.join(ASTRO_PROJECT_PATH, "src", "content", "blog")
IMAGE_SAVE_PATH = os.path.join(ASTRO_PROJECT_PATH, "public", "images", "posts")
IMAGE_PUBLIC_PATH = "/images/posts"  # URL path used in markdown
USED_TOPICS_FILE = os.path.join(ASTRO_PROJECT_PATH, "used_topics.txt")

# --- BLOG DEFAULTS ---
AUTHOR = "TechBrew Daily"