#!/usr/bin/env python3
"""Monthly Monetization Tracker & Affiliate Link Auditor for auto-content-genie system."""

import json
import pathlib
import csv
import datetime
import re

BASE = pathlib.Path("/c/Users/10/.hermes/projects/auto-content-site")
ANALYTICS = BASE / "analytics"
ARTICLES = BASE / "content" / "articles"

# Known affiliate link patterns to detect
AFFILIATE_PATTERNS = {
    "Amazon Associates": r'amazon\.com/.*/dp/[A-Za-z0-9]{10}',
    "ShareASale": r'shareasite\.com/',
    "Impact.com": r'impactradius-event\.com|impactbox\.io',
    "Generic Affiliate": r'affiliate=|ref=|^[\?&]?aid=',
}

def audit_affiliate_links_in_file(filepath: pathlib.Path) -> list:
    """Scan an HTML file for affiliate links and check if they're still placeholders."""
    content = filepath.read_text()
    issues = []
    
    # Find all link placeholders that haven't been replaced yet
    placeholder_patterns = [
        r'YOUR_PREMIUM_AFFILIATE_LINK_HERE',
        r'YOUR_BUDGET_AFFILIATE_LINK_HERE',
        r'YOUR_FREE_TIER_AFFILIATE_LINK_HERE',
        r'affiliate-link-placeholder',
    ]
    
    for pat in placeholder_patterns:
        if re.search(pat, content):
            issues.append({
                "type": "placeholder_not_replaced",
                "pattern": pat,
                "file": filepath.name,
                "severity": "ERROR",
                "message": f"Contains unreplaced placeholder: {pat}"
            })
    
    return issues

def calculate_revenue_estimates(tracker_path: str) -> dict:
    """Calculate realistic revenue projections from tracker data."""
    if not pathlib.Path(tracker_path).exists():
        return {"error": "Tracker not found"}
    
    with open(tracker_path) as f:
        tracker = json.load(f)
        
    total_articles = tracker.get("articles_published_total", 0)
    days_active = max(1, (datetime.date.today() - datetime.date.fromisoformat(tracker["start_date"])).days) + 1
    
    # Conservative / realistic / optimistic models
    conservative = {
        "monthly_traffic": int(total_articles * 45),
        "monthly_revenue": int(total_articles * 0.75)  # ~$0.75 per article/month average
    }
    
    realistic = {
        "monthly_traffic": int(total_articles * 120),
        "monthly_revenue": int(total_articles * 2.5)  # ~$2.50 per article/month avg
    }
    
    optimistic = {
        "monthly_traffic": int(total_articles * 350),  
        "monthly_revenue": int(total_articles * 6.0)   # ~$6 per article/month if high-value niches selected right
    }
    
    return {
        "days_active": days_active,
        "total_articles_published": total_articles,
        "progress_estimate": f"{int(min(100, (days_active / 450) * 100))}%",  # % toward $3k goal at day 450
        "conservative": conservative,
        "realistic": realistic,
        "optimistic": optimistic
    }

def main():
    print("=" * 60)
    print(f"MONTHLY MONETIZATION AUDIT - {datetime.date.today().isoformat()}")
    print("=" * 60)
    
    # Audit all articles for affiliate link issues
    all_issues = []
    article_list = list(ARTICLES.glob("*.html")) if ARTICLES.exists() else []
    
    print(f"\nScanning {len(article_list)} published articles...")
    for art in article_list[:50]:  # First 50 only to avoid massive output
        issues = audit_affiliate_links_in_file(art)
        all_issues.extend(issues)
        
        if issues:
            print(f"  ⚠️ {art.name}: {len(issues)} issue(s)")
    
    # Revenue estimates
    tracker_path = str(ANALYTICS / "tracker.json")
    estimates = calculate_revenue_estimates(tracker_path)
    
    if "error" not in estimates:
        total_art = estimates["total_articles_published"]
        print(f"\n{'='*40}")
        print(f"REVENUE PROJECTIONS (based on {total_art} articles):")
        print(f"{'='*40}")
        
        for model_name in ["conservative", "realistic", "optimistic"]:
            est_data = estimates[model_name]
            rev = est_data.get("monthly_revenue", 0)
            if rev > 0:
                months_to_3k = max(1, int(3000 / rev))
                time_str = f"{months_to_3k} months"
            else:
                time_str = "N/A (no revenue yet)"
            
            print(f"\n{model_name.upper()} MODEL:")
            print(f"  Monthly Traffic: ${est_data['monthly_traffic']:,.0f}")
            print(f"  Monthly Revenue: ${est_data['monthly_revenue']:,.0f}/mo")
            print(f"  Est. time to $3k/mo: {time_str}")
    
    # Summary stats  
    print(f"\n{'='*40}")
    print("AUDIT SUMMARY:")
    print(f"  Total Articles: {len(article_list)}")
    print(f"  Issues Found: {len(all_issues)}") 
    
    # Write report (inside main function, correctly indented)
    report_path = ANALYTICS / f"monetization_audit_{datetime.date.today().isoformat()}.json"
    
    with open(report_path, "w") as f: 
        json.dump({
            "date": datetime.date.today().isoformat(),
            "total_articles": len(article_list),  
            "issues_found": all_issues[:10],  # Limit to first 10
            "revenue_estimates": estimates
        }, f, indent=2)  
    
    print(f"\nReport saved to: {report_path}")
    print("=" * 60)
    print("=" * 60)


if __name__ == "__main__": 
    main()
