#!/usr/bin/env python3
"""SEO Optimizer - Runs weekly to score and improve existing content on your site"""

import pathlib
import re
import json
from datetime import date, timedelta

BASE = pathlib.Path("/c/Users/10/.hermes/projects/auto-content-site")
ARTICLES = BASE / "content" / "articles"
ANALYTICS = BASE / "analytics"
META_DIR = ANALYTICS / "meta" / "article_ratings"
META_DIR.mkdir(parents=True, exist_ok=True)

# SEO scoring rules - how Google favors pages in affiliate niches
SEO_WEIGHTS = {
    "content_length": 0.25,
    "keyword_density": 0.15,
    "heading_structure": 0.10,
    "internal_links": 0.10,
    "external_links": 0.10,
    "meta_description": 0.05,
    "title_tag": 0.05,
    "readability": 0.10,
    "first_paragraph": 0.05,
}


def get_keyword_data():
    """Load our research database of high-value keywords"""
    csv_path = BASE / "research" / "topic_database.csv"
    
    with open(csv_path) as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        return []
    
    data_lines = [line.strip().split(",") for line in lines[1:] if len(line.strip()) > 0]
    
    result = []
    for d in data_lines:
        if len(d) >= 7:
            keyword, category, vol, intent, comm, diff_score, mon_score = [
                d[i].strip() if i < len(d) else "" for i in range(7)
            ]
            result.append({
                "keyword": keyword,
                "category": category,
                "volume": int(vol),
                "intent": intent,
                "commission_range": comm,
                "difficulty": diff_score,
                "monetization_score": float(mon_score)
            })
    
    return result


def calculate_seo_score(article_html_content, primary_keyword):
    """Score an article's SEO readiness (0-10)"""
    
    score = 0
    
    # Content length (max weight 2.5)
    word_count = len(article_html_content.split())
    if word_count >= 2800:
        score += 2.5
    elif word_count >= 2000:
        score += 2.0
    elif word_count >= 1500:
        score += 1.5
    elif word_count >= 1000:
        score += 1.0
    else:
        score += 0.5
    
    # Keyword density (max weight 1.5)
    kw_lower = primary_keyword.lower()
    kw_count = article_html_content.lower().count(kw_lower)
    total_words_article = len(article_html_content.split())
    
    if total_words_article > 0:
        keyword_density = (kw_count / total_words_article) * 100
        if 1.5 <= keyword_density <= 3.0:
            score += 1.5
        elif keyword_density <= 5.0:
            score += 1.2
    
    # Heading structure (max weight 1.0)
    has_h1 = bool(re.search(r'<h1[^>]*>', article_html_content))
    h_count = re.findall(r'<h[2-4][^>]*>', article_html_content)
    score += min(1.0, len(h_count) / 5.0 if has_h1 else 0)
    
    # Internal links (max weight 1.0)
    internal_link_count = len(re.findall(r'<a\s+href="\/', article_html_content))
    score += min(1.0, internal_link_count / 3.0)
    
    # External authority links (max weight 1.0)  
    external_links = len(re.findall(r'<a\s+href="https?://(?:[^/]+\.com)/', article_html_content))
    score += min(1.0, external_links / 2.0) if external_links >= 1 else 0.3
    
    # Meta tags (combined max weight 1.0)
    has_meta_title = bool(re.search(r'<title>', article_html_content, re.IGNORECASE))
    has_meta_desc = bool(re.search(r'<meta\s+name=["\']description["\']', article_html_content, re.IGNORECASE))
    
    score += (0.5 if has_meta_title else 0) + (0.5 if has_meta_desc else 0)
    
    # Normalize to 0-10 scale
    final_score = min(10, score * (10 / max(score, 0.1)))
    
    return final_score


def generate_seo_report():
    """Generate weekly SEO optimization report"""
    articles = list(ARTICLES.glob("*.html")) if ARTICLES.exists() else []
    keyword_data = get_keyword_data()
    
    if not articles:
        print("No articles found to optimize yet.")
        return
        
    # Score each article against our best matching keywords
    article_ratings = {
        "week_of": date.today().isoformat(), 
        "total_articles": len(articles),
        "ratings": []
    }
    
    for article_path in articles:
        content = article_path.read_text()
        
        # Find the primary keyword
        title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
        h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content, re.IGNORECASE)
        
        primary_kw_matched = None  
        best_score = 0
        
        if title_match:
            title_text = title_match.group(1).lower()
            for kw_entry in keyword_data:
                if kw_entry["keyword"].lower() in title_text or \
                   any(word in title_text for word in kw_entry["keyword"].split()[:2]):
                    if kw_entry["monetization_score"] > best_score:
                        best_score = kw_entry["monetization_score"]
                        primary_kw_matched = kw_entry["keyword"]
        
        # Fallback: try first h1 content
        if not primary_kw_matched and h1_match:
            h1_text = h1_match.group(1).lower()
            for kw in keyword_data:
                if kw["keyword"].lower() in h1_text or \
                   any(w.lower() in h1_text for w in kw["keyword"].split()[:2]):
                    if kw["monetization_score"] > best_score:  
                        best_score = kw["monetization_score"]
                        primary_kw_matched = kw["keyword"]
        
        # If still no match use first keyword as placeholder
        if not primary_kw_matched and len(keyword_data) > 0:
            primary_kw_matched = keyword_data[0]["keyword"]
        
        seo_score = calculate_seo_score(content, primary_kw_matched or "placeholder")
        
        rating_entry = {
            "article_id": article_path.stem,
            "file_path": str(article_path), 
            "raw_file_name": article_path.name,
            "estimated_word_count": len(content.split()),
            "seo_score": round(seo_score, 1),
            "matched_keyword": primary_kw_matched or "Unknown",
            "keyword_monetization_potential": best_score if best_score > 0 else "N/A",
            "status": "good" if seo_score >= 7.5 else ("needs_improvement" if seo_score >= 5.0 else "needs_redesign")
        }
        
        article_ratings["ratings"].append(rating_entry)
    
    # Save report
    report_path = META_DIR / f"seo_report_{date.today().isoformat()}.json"
    with open(report_path, "w") as f:
        json.dump(article_ratings, f, indent=2)
        
    # Print summary
    total_scored = len(article_ratings["ratings"])
    
    print(f"\n=== SEO Report for {date.today().isoformat()} ===\n")
    print(f"Total articles scored: {total_scored}")
    
    ratings_list = article_ratings["ratings"]
    avg_score = sum([r["seo_score"] for r in ratings_list]) / max(len(ratings_list), 1)
    
    for rating in ratings_list:
        if rating["status"] == "good":
            status_emoji = "GOOD"
        elif rating["status"] == "needs_improvement":
            status_emoji = "NEEDS IMPROVEMENT"  
        else:
            status_emoji = "NEEDS REDESIGN"
        
        print(f"\n{status_emoji}: {rating['raw_file_name']}")
        print(f"   SEO Score: {rating['seo_score']}/10 (Best match keyword: {rating['matched_keyword']}") 
        print(f"   Est word count: {rating['estimated_word_count']} words\n")

    if avg_score < 7.0:
        print("\nAverage score is below target (7.0). Recommend:")
        print(" - Add more internal links between your articles")
        print(" - Include primary keyword in first 100 words where missing")  
        print(" - Expand short articles to at least 2000+ words each")
        
    if avg_score < 9.0: 
        print("\nNot all articles have optimal SEO settings. Consider:")
        print(" - Adding explicit meta descriptions matching search intent")
        print(" - Including 2-3 outbound links to authoritative sites per article")
    
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    generate_seo_report()
