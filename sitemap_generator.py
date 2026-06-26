#!/usr/bin/env python3
"""
Sitemap generator for VMDProjects.github.io
Creates XML sitemap for search engine indexing
"""

import os
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = "articles"
SITEMAP_FILE = "sitemap.xml"
TRACKING_FILE = "logs/generated_articles.json"
BASE_URL = "https://vmdprojects.github.io"

def generate_sitemap():
    """Generate sitemap.xml from articles directory"""
    
    urls = [
        # Home page - highest priority
        {
            "loc": f"{BASE_URL}/",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "priority": "1.0",
            "changefreq": "daily"
        }
    ]
    
    # Add all generated articles
    if os.path.exists(OUTPUT_DIR):
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(".html"):
                slug = filename.replace(".html", "")
                file_path = os.path.join(OUTPUT_DIR, filename)
                
                # Get file modification date
                mtime = os.path.getmtime(file_path)
                lastmod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                
                urls.append({
                    "loc": f"{BASE_URL}/articles/{slug}.html",
                    "lastmod": lastmod,
                    "priority": "0.8",
                    "changefreq": "weekly"
                })
    
    # Generate XML
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_header += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    xml_body = ""
    for url in urls:
        xml_body += f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
  </url>
"""
    
    xml_footer = '</urlset>'
    
    sitemap_content = xml_header + xml_body + xml_footer
    
    # Write sitemap
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    
    print(f"✓ Sitemap generated: {SITEMAP_FILE} ({len(urls)} URLs)")
    return True

if __name__ == "__main__":
    generate_sitemap()
