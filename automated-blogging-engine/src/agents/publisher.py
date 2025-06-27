import subprocess
import os  # Import the os module
from src.config import settings
from datetime import datetime

def commit_and_push_changes(commit_message: str):
    """Adds, commits, and pushes all changes in the Astro project repo."""
    print("\n--- Committing all new posts and images to GitHub ---")
    try:
        repo_path = settings.ASTRO_PROJECT_PATH
        
        # FIX: Create a list of paths to add and only include the image path if it exists
        paths_to_add = [settings.POSTS_PATH, settings.USED_TOPICS_FILE]
        if os.path.exists(settings.IMAGE_SAVE_PATH):
            paths_to_add.append(settings.IMAGE_SAVE_PATH)

        subprocess.run(["git", "add"] + paths_to_add, cwd=repo_path, check=True)
        
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        
        print("✅ All posts and images pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"❌ A Git command failed: {e}")
    except FileNotFoundError:
        print("❌ Error: 'git' command not found. Is Git installed and in your system's PATH?")