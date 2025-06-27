import re
from datetime import datetime
from src.config.settings import ASTRO_PROJECT_PATH
from src.config.categories import CATEGORIES
from src.agents import trend_spotter, content_writer, art_director, publisher
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
        
        content_with_placeholders = content_writer.write_blog_post(topic, category_obj)
        if not content_with_placeholders:
            print("⚠️  Failed to generate content. Skipping.")
            continue
        
        post_slug = file_handler.generate_slug(topic)
        if not post_slug:
            continue

        # Generate the main hero image first
        hero_image_prompt = f"A vibrant and detailed hero image for a tech blog post titled '{topic}'"
        hero_image_url = art_director.generate_and_save_image(hero_image_prompt, post_slug)
        
        # Replace the placeholder in the frontmatter
        # FIX: Add a fallback URL if image generation fails
        final_hero_url = hero_image_url if hero_image_url else "/images/posts/placeholder.png"
        content_with_placeholders = content_with_placeholders.replace("[IMAGE_URL_PLACEHOLDER]", final_hero_url)

        # Process secondary images in the content body
        final_content = content_with_placeholders
        secondary_image_prompts = re.findall(r'\[IMAGE: (.*?)\]', content_with_placeholders)
        
        if secondary_image_prompts:
            print(f"🖼️  Found {len(secondary_image_prompts)} secondary image prompts. Generating...")
            for img_prompt in secondary_image_prompts:
                image_public_url = art_director.generate_and_save_image(img_prompt, post_slug)
                # FIX: Only replace the placeholder if the image was created successfully
                if image_public_url:
                    img_markdown = f'\n![{img_prompt.split(",")[0]}]({image_public_url})\n'
                    final_content = final_content.replace(f'[IMAGE: {img_prompt}]', img_markdown, 1)
                else:
                    # If it fails, remove the placeholder tag entirely
                    final_content = final_content.replace(f'[IMAGE: {img_prompt}]', '', 1)
        
        # Save the final file with all images processed
        file_handler.save_markdown_file(final_content, post_slug)
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