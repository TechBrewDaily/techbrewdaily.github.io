#!/usr/bin/env python3
"""
TechBrew Daily - Strategic SEO Content Generator
Targets specific high-value keywords for Google first-page rankings
"""

import os
import sys
import google.generativeai as genai
from datetime import datetime
import json
import random

# High-value keyword targets for Indian tech market
TARGET_KEYWORDS = [
    {
        "keyword": "AI in India 2025",
        "intent": "informational",
        "topic": "Complete Guide to Artificial Intelligence Adoption in Indian Industries 2025"
    },
    {
        "keyword": "Indian tech startups",
        "intent": "informational", 
        "topic": "Top 50 Indian Tech Startups to Watch in 2025: Funding, Valuations & Growth"
    },
    {
        "keyword": "fintech India latest news",
        "intent": "news",
        "topic": "Latest Fintech Trends Transforming Indian Banking and Payments in 2025"
    },
    {
        "keyword": "technology trends India",
        "intent": "informational",
        "topic": "Major Technology Trends Reshaping Indian Business Landscape in 2025"
    },
    {
        "keyword": "startup funding India",
        "intent": "commercial",
        "topic": "Ultimate Guide to Startup Funding in India 2025: From Seed to IPO"
    },
    {
        "keyword": "mobile app development India",
        "intent": "commercial",
        "topic": "Complete Guide to Mobile App Development in India: Costs, Companies & Trends 2025"
    },
    {
        "keyword": "digital transformation India",
        "intent": "informational",
        "topic": "Digital Transformation Strategies for Indian Businesses: Success Stories & Roadmap 2025"
    },
    {
        "keyword": "machine learning India",
        "intent": "educational",
        "topic": "Machine Learning in India 2025: Career Guide, Salaries & Top Companies"
    }
]

def setup_api():
    """Setup Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        return False
    
    genai.configure(api_key=api_key)
    return True

def generate_strategic_content(keyword_data):
    """Generate content targeting specific keywords for rankings"""
    
    keyword = keyword_data["keyword"]
    topic = keyword_data["topic"]
    intent = keyword_data["intent"]
    
    print(f"🎯 Generating content for keyword: '{keyword}'")
    print(f"📝 Topic: {topic}")
    
    # Generate SEO title
    title_prompt = f"""
    Create the PERFECT SEO title for ranking #1 on Google for the keyword: "{keyword}"
    
    Topic: "{topic}"
    Search Intent: {intent}
    Target: Indian audience
    
    Requirements:
    - 50-60 characters exactly
    - Include exact keyword "{keyword}"
    - Compelling for clicks
    - Professional and authoritative
    - Include year 2025 if relevant
    - Use power words: Complete, Ultimate, Best, Top, Guide, Latest
    
    Return ONLY the title, nothing else.
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        title_response = model.generate_content(title_prompt)
        seo_title = title_response.text.strip().replace('"', "'")
        
        # Generate meta description
        desc_prompt = f"""
        Create the PERFECT meta description for the keyword: "{keyword}"
        Title: "{seo_title}"
        
        Requirements:
        - 150-160 characters exactly
        - Include keyword "{keyword}" naturally
        - Compelling call-to-action
        - Promise specific value
        - Target Indian professionals
        
        Return ONLY the description, nothing else.
        """
        
        desc_response = model.generate_content(desc_prompt)
        meta_desc = desc_response.text.strip().replace('"', "'")
        
        # Generate comprehensive content
        content_prompt = f"""
        Write a comprehensive, SEO-optimized article targeting the keyword: "{keyword}"
        
        Title: "{seo_title}"
        Topic: "{topic}"
        Search Intent: {intent}
        Target Audience: Indian tech professionals, entrepreneurs, students
        
        CRITICAL SEO REQUIREMENTS:
        - TARGET KEYWORD DENSITY: Use "{keyword}" 8-12 times naturally throughout content
        - WORD COUNT: 2000-2500 words for maximum SEO impact
        - LSI KEYWORDS: Include related terms like "artificial intelligence India", "tech companies India", "innovation India", "startup ecosystem India"
        - CURRENT YEAR: Include "2025" frequently for freshness signals
        - INDIAN CONTEXT: Use Indian company examples, statistics, and market data
        
        CONTENT STRUCTURE (MANDATORY):
        1. Hook paragraph with keyword in first sentence
        2. Table of Contents (markdown list)
        3. Introduction explaining what readers will learn
        4. 6-8 main sections with H2 headings (include keyword in 2-3 headings)
        5. Each section 300-400 words with practical insights
        6. "Why This Matters for India" section
        7. "Industry Expert Insights" section with quotes
        8. "Frequently Asked Questions" (8-10 detailed Q&As with keyword variations)
        9. "Key Takeaways" bullet point list
        10. Strong conclusion with actionable next steps
        
        ADVANCED SEO TECHNIQUES:
        - Use question-based H3 headings for voice search
        - Include numbered and bulleted lists
        - Add comparison tables where relevant
        - Use transition words for readability
        - Include specific statistics and data points
        - Create scannable content with short paragraphs
        
        WRITING REQUIREMENTS:
        - Professional, authoritative tone
        - Include real Indian companies as examples
        - Add realistic market statistics
        - Provide actionable, practical advice
        - Address specific Indian market challenges
        - Use active voice and clear language
        
        RESTRICTIONS:
        - NO frontmatter or YAML
        - NO main title as H1
        - Start with introduction paragraph
        - NO image references
        - Be factually accurate
        - Provide genuine value
        
        Begin writing immediately:
        """
        
        content_response = model.generate_content(content_prompt)
        content = content_response.text.strip()
        
        # Clean content
        lines = content.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            if line.startswith('# ') or (i < 3 and seo_title.lower() in line.lower()):
                continue
            cleaned_lines.append(line)
        
        final_content = '\n'.join(cleaned_lines).strip()
        
        return seo_title, meta_desc, final_content
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return None, None, None

def save_strategic_post(title, description, content, keyword):
    """Save strategically optimized post"""
    
    if not content:
        return False
    
    # Generate filename from keyword
    filename_base = keyword.lower().replace(" ", "-").replace("2025", "2025")
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    # Generate comprehensive tags
    tags = ["technology", "india", "2025", "tech-news"]
    
    # Add keyword-specific tags
    if "ai" in keyword.lower():
        tags.extend(["artificial-intelligence", "machine-learning", "ai-india"])
    if "startup" in keyword.lower():
        tags.extend(["startups", "entrepreneurship", "funding", "unicorns"])
    if "fintech" in keyword.lower():
        tags.extend(["fintech", "digital-payments", "banking", "finance"])
    if "mobile" in keyword.lower():
        tags.extend(["mobile-development", "apps", "android", "ios"])
    if "digital transformation" in keyword.lower():
        tags.extend(["digital-transformation", "business", "automation"])
    
    tags = list(dict.fromkeys(tags))[:10]
    tags_yaml = "\n".join([f'  - "{tag}"' for tag in tags])
    
    # Select random image
    images = [f"/images/blog-placeholder-{i}.svg" for i in range(1, 6)]
    selected_image = random.choice(images)
    
    # Create frontmatter
    frontmatter = f'''---
title: "{title}"
pubDate: "{date_str}"
description: "{description}"
author: "TechBrew Daily"
category: "Technology"
tags:
{tags_yaml}
image:
  url: "{selected_image}"
  alt: "Featured image for {title}"
featured: true
seo:
  targetKeyword: "{keyword}"
  canonical: ""
  noindex: false
readingTime: {len(content.split()) // 200 + 1}
---

{content}'''
    
    # Save file
    blog_folder = os.path.join("src", "content", "blog")
    os.makedirs(blog_folder, exist_ok=True)
    
    filename = f"strategic-seo-{filename_base}.md"
    filepath = os.path.join(blog_folder, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter)
        
        word_count = len(content.split())
        print(f"✅ Strategic SEO post saved: {filename}")
        print(f"🎯 Target keyword: {keyword}")
        print(f"📊 Word count: {word_count}")
        print(f"⏱️  Reading time: {word_count // 200 + 1} minutes")
        
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def main():
    """Generate strategic SEO content for target keywords"""
    
    print("🎯 TechBrew Daily - Strategic SEO Content Generator")
    print("Targeting high-value keywords for Google #1 rankings")
    print("=" * 60)
    
    if not setup_api():
        return
    
    # Generate content for each target keyword
    for i, keyword_data in enumerate(TARGET_KEYWORDS, 1):
        try:
            print(f"\n📈 [{i}/{len(TARGET_KEYWORDS)}] Processing keyword strategy...")
            
            title, description, content = generate_strategic_content(keyword_data)
            
            if title and description and content:
                success = save_strategic_post(title, description, content, keyword_data["keyword"])
                if success:
                    print(f"✅ Content generated for: {keyword_data['keyword']}")
                else:
                    print(f"❌ Failed to save content for: {keyword_data['keyword']}")
            else:
                print(f"❌ Failed to generate content for: {keyword_data['keyword']}")
            
            # Small delay to avoid rate limiting
            import time
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error processing {keyword_data['keyword']}: {e}")
            continue
    
    print(f"\n🎉 Strategic SEO content generation complete!")
    print("🚀 Your website is now optimized to rank for high-value Indian tech keywords!")
    print("\n📊 Next steps:")
    print("1. Run 'npm run build' to build the site")
    print("2. Deploy to production")
    print("3. Submit sitemap to Google Search Console")
    print("4. Monitor rankings in 2-4 weeks")

if __name__ == "__main__":
    main()
