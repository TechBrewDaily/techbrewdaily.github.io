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
    """Check if the site is healthy"""
    print(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Checking site health...")
    
    try:
        # Build the site to check for errors
        result = subprocess.run([
            "npm", "run", "build"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Site health check passed")
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
    
    print("📈 Weekly SEO Report Complete")
    print("💡 Next steps:")
    print("   1. Check Google Search Console for new rankings")
    print("   2. Monitor organic traffic growth")
    print("   3. Update content based on trending topics")

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
