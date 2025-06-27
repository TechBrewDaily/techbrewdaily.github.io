import os
from dotenv import load_dotenv

# Load environment variables from a .env file in the project root
load_dotenv()

# --- API KEYS ---
GEMINI_API_KEY_TOPICS = os.getenv("GEMINI_API_KEY_1")
GEMINI_API_KEY_CONTENT = os.getenv("GEMINI_API_KEY_2")
# Removed image API key since we're not using images

# --- PATHS ---
# Use an environment variable for the path in production (GitHub Actions),
# with a fallback to the local relative path for development.
# In GitHub Actions, GITHUB_WORKSPACE will be the root repository path
# Locally, we find the parent directory of the current script's project.
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ASTRO_PROJECT_PATH = os.getenv('GITHUB_WORKSPACE', os.path.dirname(_project_root))

# Paths within the Astro project
POSTS_PATH = os.path.join(ASTRO_PROJECT_PATH, "src", "content", "blog")
USED_TOPICS_FILE = os.path.join(ASTRO_PROJECT_PATH, "used_topics.txt")

# --- BLOG DEFAULTS ---
AUTHOR = "TechBrew Daily"