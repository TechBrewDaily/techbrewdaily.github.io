import os
from src.config import settings

def load_used_topics() -> set:
    """Loads the set of used topics from the tracking file."""
    if not os.path.exists(settings.USED_TOPICS_FILE):
        return set()
    with open(settings.USED_TOPICS_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_used_topics(topics_set: set):
    """Saves the updated set of topics back to the tracking file."""
    with open(settings.USED_TOPICS_FILE, 'w', encoding='utf-8') as f:
        for topic in sorted(list(topics_set)):
            f.write(topic + '\n')
    print("📝 Updated used topics list.")