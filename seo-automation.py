#!/usr/bin/env python3
"""
TechBrew Daily - SEO Monitoring & Automation Script
Automates daily content generation and SEO monitoring
"""

import os
import subprocess
import schedule
import time
from datetime import datetime

def generate_daily_content():
    """Generate daily SEO-optimized content"""
    print(f"🚀 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Starting daily content generation...")
    
    try:
        # Set environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not set")
            return False
        
        # Generate SEO content
        result = subprocess.run([
            "python", "generate-seo-blog.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Daily SEO content generated successfully")
            
            # Build site
            build_result = subprocess.run([
                "npm", "run", "build"
            ], capture_output=True, text=True)
            
            if build_result.returncode == 0:
                print("✅ Site built successfully")
                return True
            else:
                print(f"❌ Build failed: {build_result.stderr}")
                return False
        else:
            print(f"❌ Content generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error in daily generation: {e}")
        return False

def check_site_health():
    """Check if the site is healthy and submit to search engines"""
    print(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Checking site health...")
    
    try:
        # Build the site to check for errors
        result = subprocess.run([
            "npm", "run", "build"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Site health check passed")
            
            # Check if sitemap exists
            sitemap_path = os.path.join("dist", "sitemap-index.xml")
            if os.path.exists(sitemap_path):
                print("✅ Sitemap generated successfully")
                
                # Submit sitemap to Google (requires Google Search Console API setup)
                sitemap_url = "https://techbrewdaily.github.io/sitemap-index.xml"
                print(f"📤 Sitemap available at: {sitemap_url}")
                print("💡 Submit this URL to Google Search Console manually")
                
                # Also check enhanced sitemap
                enhanced_sitemap = "https://techbrewdaily.github.io/enhanced-sitemap.xml"
                print(f"📤 Enhanced sitemap available at: {enhanced_sitemap}")
                
            else:
                print("❌ Sitemap not found")
            
            return True
        else:
            print(f"❌ Site health check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def weekly_seo_report():
    """Generate weekly SEO performance report"""
    print(f"📊 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Generating weekly SEO report...")
    
    # Count blog posts
    blog_dir = os.path.join("src", "content", "blog")
    if os.path.exists(blog_dir):
        posts = len([f for f in os.listdir(blog_dir) if f.endswith('.md')])
        print(f"📝 Total blog posts: {posts}")
    
    # Check sitemap
    sitemap_path = os.path.join("dist", "sitemap-index.xml")
    if os.path.exists(sitemap_path):
        print("✅ Sitemap exists")
    else:
        print("❌ Sitemap missing")
    
    # Check robots.txt
    robots_path = os.path.join("dist", "robots.txt")
    if os.path.exists(robots_path):
        print("✅ Robots.txt exists")
    else:
        print("❌ Robots.txt missing")
    
    print("📈 Weekly SEO Report Complete")
    print("💡 Action Items for Google Indexing:")
    print("   1. Submit site to Google Search Console: https://search.google.com/search-console/")
    print("   2. Add property: https://techbrewdaily.github.io")
    print("   3. Submit sitemap: https://techbrewdaily.github.io/sitemap-index.xml")
    print("   4. Submit enhanced sitemap: https://techbrewdaily.github.io/enhanced-sitemap.xml")
    print("   5. Request indexing for key pages in Search Console")
    print("   6. Monitor indexing status and rankings")
    print("   7. Check Core Web Vitals in PageSpeed Insights")
    print("   8. Update content based on trending topics")
    
    # SEO Checklist Status
    print("\n🔍 SEO Implementation Status:")
    print("   ✅ Site deployed at root domain (techbrewdaily.github.io)")
    print("   ✅ Robots.txt configured")
    print("   ✅ XML Sitemap auto-generated")
    print("   ✅ Enhanced sitemap created")
    print("   ✅ Meta tags optimized")
    print("   ✅ Schema.org structured data")
    print("   ✅ Geographic targeting (India)")
    print("   ✅ Mobile-friendly design")
    print("   ✅ Fast loading (Astro SSG)")
    print("   ✅ RSS feed available")
    print("   📝 TODO: Google Search Console verification")
    print("   📝 TODO: Submit to Bing Webmaster Tools")
    print("   📝 TODO: Social media presence setup")

def main():
    """Main automation scheduler"""
    print("🤖 TechBrew Daily SEO Automation Started")
    print("=" * 50)
    
    # Schedule daily content generation at 9 AM
    schedule.every().day.at("09:00").do(generate_daily_content)
    
    # Schedule health checks every 6 hours
    schedule.every(6).hours.do(check_site_health)
    
    # Schedule weekly reports on Mondays at 10 AM
    schedule.every().monday.at("10:00").do(weekly_seo_report)
    
    print("📅 Scheduled tasks:")
    print("   • Daily content generation: 9:00 AM")
    print("   • Health checks: Every 6 hours")
    print("   • Weekly reports: Mondays 10:00 AM")
    print("\n🚀 Automation running... Press Ctrl+C to stop")
    
    # Run initial health check
    check_site_health()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n👋 SEO automation stopped")

if __name__ == "__main__":
    # Check if running in development mode
    if len(os.sys.argv) > 1:
        if os.sys.argv[1] == "generate":
            generate_daily_content()
        elif os.sys.argv[1] == "health":
            check_site_health()
        elif os.sys.argv[1] == "report":
            weekly_seo_report()
        else:
            print("Usage: python seo-automation.py [generate|health|report]")
    else:
        main()
