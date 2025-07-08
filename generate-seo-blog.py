#!/usr/bin/env python3
"""
TechBrew Daily - Advanced SEO Blog Generator
Generates high-quality, SEO-optimized blog posts for better Google rankings.
"""

import os
import sys
import google.generativeai as genai
import feedparser
from datetime import datetime
import json
import re
import random

# --- CONFIG ---
AUTHOR = "TechBrew Daily Team"
BLOG_FOLDER = os.path.join("src", "content", "blog")

# --- SEO TOPICS DATABASE ---
HIGH_VALUE_TOPICS = [
    "AI adoption in Indian enterprises 2025",
    "Fintech revolution transforming Indian banking",
    "Top mobile app development trends India",
    "Blockchain technology in Indian startups",
    "Digital transformation strategies for Indian businesses",
    "Machine learning applications in Indian healthcare",
    "Cybersecurity challenges for Indian companies",
    "EdTech innovations revolutionizing Indian education",
    "Electric vehicle technology in Indian automotive",
    "Smart city initiatives across Indian metros",
    "Indian unicorn startups funding trends",
    "5G technology rollout impact in India",
    "Cloud computing adoption by Indian SMEs",
    "Indian developer tools and programming trends",
    "Sustainable technology solutions in India"
]

# --- SETUP ---
def setup_gemini():
    """Configure the Gemini API Key"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ Error: GEMINI_API_KEY environment variable not set")
            print("Please set your Gemini API key:")
            print("export GEMINI_API_KEY='your_api_key_here'")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured successfully")
        return True
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {e}")
        return False

def fetch_trending_topic():
    """Fetches the latest tech news or uses curated topics."""
    print("🔍 Fetching trending topic...")
    
    try:
        # Try to fetch from Google News first
        feed = feedparser.parse("https://news.google.com/rss/search?q=technology+india+startup+AI&hl=en-IN&gl=IN&ceid=IN:en")
        if feed.entries and len(feed.entries) > 0:
            # Get a random entry from the first 5 to add variety
            entry = random.choice(feed.entries[:5])
            topic = entry.title
            print(f"📰 Found trending topic: {topic}")
            return topic
    except Exception as e:
        print(f"⚠️  Could not fetch news feed: {e}")
    
    # Fallback to curated high-value topics
    topic = random.choice(HIGH_VALUE_TOPICS)
    print(f"🎯 Using curated topic: {topic}")
    return topic

def generate_seo_metadata(topic):
    """Generates SEO-optimized title and meta description."""
    print(f"✍️  Generating SEO metadata for: '{topic}'")
    
    prompt = f"""
    Create a highly SEO-optimized title and meta description for a tech blog post.
    
    Topic: "{topic}"
    Target Audience: Indian tech professionals, entrepreneurs, developers
    Target Year: 2025
    
    TITLE Requirements:
    - 50-60 characters maximum
    - Include primary keyword from topic
    - Be compelling for Indian tech audience
    - Include "2025" if relevant
    - Use power words: "Complete Guide", "Ultimate", "Best", "Top", "How to", "Latest"
    - Focus on value and benefits
    - Avoid clickbait, be professional
    
    META DESCRIPTION Requirements:
    - 150-160 characters maximum
    - Include primary keyword and 1-2 secondary keywords
    - Clear value proposition
    - Mention India/Indian when relevant
    - Strong call-to-action
    - Professional and compelling
    
    EXAMPLES of good titles:
    - "Complete AI Guide for Indian Businesses 2025"
    - "Top 15 Fintech Trends Reshaping Indian Banking"
    - "Ultimate Startup Funding Guide for India 2025"
    
    Return ONLY valid JSON:
    {{"title": "Your SEO Title", "description": "Your meta description here."}}
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        cleaned_json = response.text.strip().replace("```json", "").replace("```", "")
        
        try:
            metadata = json.loads(cleaned_json)
            title = metadata['title'][:60]  # Ensure length limit
            description = metadata['description'][:160]  # Ensure length limit
            return title, description
        except json.JSONDecodeError:
            print("⚠️  Could not parse JSON response, using fallback")
            fallback_title = f"Complete Guide: {topic} in India 2025"[:60]
            fallback_desc = f"Discover everything about {topic} in India. Expert insights, trends, and practical tips for 2025."[:160]
            return fallback_title, fallback_desc
            
    except Exception as e:
        print(f"❌ Error generating metadata: {e}")
        fallback_title = f"Complete Guide: {topic} in India 2025"[:60]
        fallback_desc = f"Expert insights on {topic} for Indian professionals. Latest trends and practical guidance."[:160]
        return fallback_title, fallback_desc

def generate_seo_content(topic, seo_title):
    """Generates comprehensive, SEO-optimized blog content."""
    print(f"🧠 Generating SEO-optimized content for: '{seo_title}'")
    
    prompt = f"""
    Write a comprehensive, SEO-optimized tech blog post for Indian readers.
    
    Original Topic: "{topic}"
    SEO Title: "{seo_title}"
    Target Audience: Indian tech professionals, entrepreneurs, students
    Target Market: India
    Current Year: 2025
    
    SEO OPTIMIZATION REQUIREMENTS:
    - 1500-2000 words for maximum SEO impact
    - Natural keyword integration (1-2% density)
    - Include semantic keywords and related terms
    - Structure for featured snippets potential
    - Include current year (2025) where relevant
    - Add specific Indian context and examples
    
    CONTENT STRUCTURE (MANDATORY):
    1. **Hook & Introduction** (2-3 sentences + value proposition paragraph)
    2. **Table of Contents** (markdown list of main sections)
    3. **4-6 Main Sections** with H2 headings (##)
    4. **Subsections** with H3 headings (###) where needed
    5. **"Frequently Asked Questions"** section with 5-6 detailed Q&As
    6. **"Key Takeaways"** section with bullet points
    7. **Strong Conclusion** with actionable next steps
    
    WRITING REQUIREMENTS:
    - Professional, authoritative tone
    - Include real Indian companies/examples where appropriate
    - Add realistic statistics and data points
    - Use numbered lists and bullet points
    - Keep paragraphs 2-4 sentences
    - Include practical, actionable advice
    - Use transition words for readability
    - Address Indian market specifically
    
    CONTENT GUIDELINES:
    - Be factually accurate and professional
    - Include latest 2025 trends and predictions
    - Provide genuine value and insights
    - Use clear, accessible language
    - Include specific examples and case studies
    - Address common challenges and solutions
    
    CRITICAL RESTRICTIONS:
    - Do NOT include YAML frontmatter
    - Do NOT include the main title as H1
    - Start directly with the introduction
    - Do NOT include image references
    - Use only H2 (##) and H3 (###) headings
    - Ensure all information is helpful and accurate
    
    Begin writing immediately with the introduction:
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up any accidentally generated titles
        lines = content.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            # Remove H1 titles or title references in first few lines
            if (line.startswith('# ') or 
                (i < 5 and line.strip() and seo_title.lower() in line.lower() and line.strip().startswith('*'))):
                print(f"🧹 Removing title line: {line[:50]}...")
                continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines).strip()
        
        # Validate content length
        word_count = len(content.split())
        if word_count < 800:
            print(f"⚠️  Warning: Content is only {word_count} words (target: 1500+)")
        else:
            print(f"✅ Generated {word_count} words of content")
        
        return content
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return ""

def generate_seo_tags(title):
    """Generate relevant SEO tags based on title content."""
    tags = ["technology", "india", "tech-news", "innovation", "2025"]
    
    title_lower = title.lower()
    
    # AI and Machine Learning
    if any(keyword in title_lower for keyword in ["ai", "artificial intelligence", "machine learning", "ml"]):
        tags.extend(["ai", "artificial-intelligence", "machine-learning", "automation"])
    
    # Startups and Business
    if any(keyword in title_lower for keyword in ["startup", "business", "entrepreneur", "company"]):
        tags.extend(["startup", "entrepreneurship", "business", "funding"])
    
    # Fintech and Finance
    if any(keyword in title_lower for keyword in ["fintech", "finance", "banking", "payment"]):
        tags.extend(["fintech", "finance", "banking", "digital-payments"])
    
    # Mobile and Apps
    if any(keyword in title_lower for keyword in ["mobile", "app", "android", "ios"]):
        tags.extend(["mobile-apps", "android", "ios", "mobile-development"])
    
    # Blockchain and Crypto
    if any(keyword in title_lower for keyword in ["blockchain", "crypto", "web3", "bitcoin"]):
        tags.extend(["blockchain", "cryptocurrency", "web3", "digital-currency"])
    
    # Cloud and Infrastructure
    if any(keyword in title_lower for keyword in ["cloud", "aws", "azure", "infrastructure"]):
        tags.extend(["cloud-computing", "infrastructure", "devops", "scalability"])
    
    # Development and Programming
    if any(keyword in title_lower for keyword in ["development", "programming", "code", "developer"]):
        tags.extend(["software-development", "programming", "developer-tools", "coding"])
    
    # Remove duplicates and limit to 10 tags
    tags = list(dict.fromkeys(tags))[:10]
    return tags

def save_seo_optimized_post(title, description, content):
    """Save the blog post with comprehensive SEO frontmatter."""
    if not content:
        print("❌ No content generated. Skipping save.")
        return False
    
    print("💾 Saving SEO-optimized blog post...")
    os.makedirs(BLOG_FOLDER, exist_ok=True)
    
    # Generate filename
    today = datetime.now()
    date_str = today.strftime("%Y%m%d")
    time_str = today.strftime("%H%M")
    pub_date = today.strftime("%Y-%m-%d")
    
    # Clean inputs for YAML
    safe_title = title.replace('"', "'").replace('\n', ' ').strip()
    safe_description = description.replace('"', "'").replace('\n', ' ').strip()
    
    # Generate SEO tags
    tags = generate_seo_tags(title)
    tags_yaml = "\n".join([f"  - \"{tag}\"" for tag in tags])
    
    # Select random image
    images = [
        "/images/blog-placeholder-1.svg",
        "/images/blog-placeholder-2.svg",
        "/images/blog-placeholder-3.svg",
        "/images/blog-placeholder-4.svg",
        "/images/blog-placeholder-5.svg"
    ]
    selected_image = random.choice(images)
    
    # Create comprehensive frontmatter
    frontmatter = f"""---
title: "{safe_title}"
pubDate: "{pub_date}"
description: "{safe_description}"
author: "{AUTHOR}"
category: "Technology"
tags:
{tags_yaml}
image:
  url: "{selected_image}"
  alt: "Featured image for {safe_title}"
featured: true
seo:
  canonical: ""
  noindex: false
  nofollow: false
readingTime: {len(content.split()) // 200 + 1}
---

{content}"""
    
    # Save file
    filename = f"seo-post-{date_str}-{time_str}.md"
    filepath = os.path.join(BLOG_FOLDER, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter)
        
        word_count = len(content.split())
        print(f"✅ SEO-optimized post saved: {filepath}")
        print(f"📝 Title: {title}")
        print(f"📊 Word count: {word_count}")
        print(f"🏷️  Tags: {', '.join(tags[:5])}...")
        print(f"⏱️  Estimated reading time: {word_count // 200 + 1} minutes")
        return True
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def main():
    """Main function to generate SEO-optimized blog post."""
    print("🚀 TechBrew Daily - Advanced SEO Blog Generator")
    print("=" * 50)
    
    # Setup
    if not setup_gemini():
        return
    
    try:
        # Generate content
        topic = fetch_trending_topic()
        title, description = generate_seo_metadata(topic)
        content = generate_seo_content(topic, title)
        
        # Save post
        if save_seo_optimized_post(title, description, content):
            print("\n🎉 SEO-optimized blog post generated successfully!")
            print("\n📈 SEO Tips:")
            print("- Content is optimized for search engines")
            print("- Title and meta description are within optimal lengths")
            print("- Content includes relevant keywords and Indian context")
            print("- Structure is designed for featured snippets")
            print("- FAQ section targets voice search queries")
        else:
            print("\n❌ Failed to generate blog post")
    
    except KeyboardInterrupt:
        print("\n\n👋 Generation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
