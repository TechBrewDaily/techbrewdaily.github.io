import re
from datetime import datetime
from src.config.settings import ASTRO_PROJECT_PATH
from src.config.categories import CATEGORIES
from src.agents import trend_spotter, content_writer, publisher
from src.utils import topic_tracker, file_handler

def main():
    print("🚀 Starting the TechBrew Daily Auto-Blogger Engine...")
    print(f"Operating on Astro project at: {ASTRO_PROJECT_PATH}")

    used_topics = topic_tracker.load_used_topics()
    newly_generated_topics = set()

    for category_obj in CATEGORIES:
        print(f"\n--- Processing Category: {category_obj['name']} ---")
        
        topic = trend_spotter.find_trending_topic(category_obj, used_topics.union(newly_generated_topics))
        if not topic:
            print("⚠️  Could not find a unique topic. Skipping category.")
            continue
        
        content = content_writer.write_blog_post(topic, category_obj)
        if not content:
            print("⚠️  Failed to generate content. Skipping.")
            continue
        
        post_slug = file_handler.generate_slug(topic)
        if not post_slug:
            continue

        # Save the content directly without image processing
        file_handler.save_markdown_file(content, post_slug)
        newly_generated_topics.add(topic)

    if not newly_generated_topics:
        print("\nNo new articles were generated. Exiting.")
        return

    topic_tracker.save_used_topics(used_topics.union(newly_generated_topics))
    
    commit_message = f"feat: Add {len(newly_generated_topics)} new articles for {datetime.now().strftime('%Y-%m-%d')}"
    publisher.commit_and_push_changes(commit_message)

    print("\n✅ Daily blog generation complete!")

if __name__ == "__main__":
    main()