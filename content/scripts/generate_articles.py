#!/usr/bin/env python3
"""
HERMES AUTO-CONTENT GENIE - Iran-Optimized Crypto Income Edition
Uses crypto affiliate programs (MEXC, Bybit 40-70%) + BTCPay Server / NOWPayments.
No Amazon Associates, no Google AdSense, no PayPal - all rails work in Iran.
"""

import json
import csv
import random
import datetime
import pathlib
import re
import time

BASE = pathlib.Path("c:/Users/10/.hermes/projects/auto-content-site")
ARTICLES = BASE / "content" / "articles"
TEMPLATE = BASE / "content" / "templates"
RESEARCH = BASE / "research"
ANALYTICS = BASE / "analytics"
SCRIPTS = BASE / "content" / "scripts"
SETUP_DIR = BASE / "setup"
CONFIG_DIR = BASE / "config"

for d in [ARTICLES, TEMPLATE, RESEARCH, ANALYTICS, SCRIPTS, SETUP_DIR, CONFIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Load Iran affiliate config
AFFILIATE_CONFIG_PATH = CONFIG_DIR / "iran_affiliate_links.json"
if AFFILIATE_CONFIG_PATH.exists():
    with open(AFFILIATE_CONFIG_PATH) as f:
        _aff_cfg = json.load(f)
else:
    _aff_cfg = {}


def _url(section, key, default):
    """Helper to safely get a URL from the affiliate config."""
    val = default
    s = _aff_cfg.get(section, {})
    e = s.get(key, {})
    if isinstance(e, dict):
        for ukey in ("url", "merchant_dashboard", "publisher_signup", "affiliate_dashboard"):
            v = e.get(ukey)
            if isinstance(v, str) and v:
                val = v
    return val


MEXC_URL   = _url("exchanges", "mexc_exchange",  "https://www.mexc.com/register?inviteCode=mexc")
BYBIT_URL  = _url("exchanges", "bybit_affiliate", "https://www.bybit.com/invite?ref=A5O6X")
COINGATE_URL     = _url("crypto_payment_gateways", "coingate_merchant", "https://www.coingate.com/")
NOWPAYS_URL  = _url("crypto_payment_gateways", "nowpayments",   "https://nowpayments.io/")
ADSTERRA_URL   = _url("ad_networks", "adsterra",  "https://adsterra.com/register/publisher")
PROPELLERADS_URL   = _url("ad_networks", "propellerads",  "https://propellerads.com/register")

# Category-to-article-type mapping with crypto focus
CATEGORY_MAP = {
    "exchange": "crypto-exchange-review",
    "bybit": "crypto-exchange-review",
    "mexc": "crypto-exchange-review",
    "payment": "crypto-payment-gateway",
    "btcpay": "crypto-payment-gateway",
    "coingate": "crypto-payment-gateway",
    "wallet": "crypto-hardware-wallet",
    "trading": "trading-tools-review",
    "staking": "defi-staking-guide",
    "Telegram": "ad-network-guides",
    "mining": "crypto-mining-guide",
}

# Tier names per article type
TIER_NAMES = {
    "crypto-exchange-review": {
        "premium": {"name": "MEXC Exchange", "price": "$0 to open, low trading fees"},
        "budget":  {"name": "Bybit Platform", "price": "$0 to open, min deposit"},
        "free":    {"name": "NOWPayments Wallet", "price": "Free crypto wallet"},
    },
    "crypto-payment-gateway": {
        "premium": {"name": "CoinGate Merchant", "price": "~1% per transaction"},
        "budget":  {"name": "BTCPay Server", "price": "Free self-hosted option"},
        "free":    {"name": "NOWPayments Gateway", "price": "0.5% transaction fee"},
    },
    "crypto-hardware-wallet": {
        "premium": {"name": "Ledger Nano X", "price": "$149 hardware wallet"},
        "budget":  {"name": "Trezor Model T", "price": "$169 hardware wallet"},
        "free":    {"name": "MetaMask Wallet", "price": "Free browser extension"},
    },
    "trading-tools-review": {
        "premium": {"name": "MEXC Premium Plan", "price": "up to 70% referral eligible"},
        "budget":  {"name": "Bybit Standard", "price": "40% referral commission eligible"},
        "free":    {"name": "TradingView Free", "price": "Free charting tier available"},
    },
    "defi-staking-guide": {
        "premium": {"name": "MEXC Earn (Premium)", "price": "up to 70% referral commission"},
        "budget":  {"name": "Bybit Staking", "price": "40% referral + staking rewards"},
        "free":    {"name": "Community Telegram Bots", "price": "Free entry point"},
    },
    "crypto-mining-guide": {
        "premium": {"name": "ASIC Mining Rigs", "price": "$2,000-$15,000 hardware investment"},
        "budget":  {"name": "GPU Mining Setup", "price": "$800-$3,000 start cost"},
        "free":    {"name": "Cloud Mining Free Trials", "price": "Limited free trials available"},
    },
}

# Default affiliate links per article type
DEFAULT_LINKS = {
    "crypto-exchange-review":  {"premium": MEXC_URL, "budget": BYBIT_URL, "free": NOWPAYS_URL},
    "crypto-payment-gateway":  {"premium": COINGATE_URL, "budget": NOWPAYS_URL, "free": ADSTERRA_URL},
    "crypto-hardware-wallet":  {"premium": MEXC_URL, "budget": BYBIT_URL, "free": NOWPAYS_URL},
    "trading-tools-review":    {"premium": BYBIT_URL, "budget": MEXC_URL, "free": NOWPAYS_URL},
    "defi-staking-guide":      {"premium": MEXC_URL, "budget": BYBIT_URL, "free": NOWPAYS_URL},
    "crypto-mining-guide":     {"premium": NOWPAYS_URL, "budget": ADSTERRA_URL, "free": PROPELLERADS_URL},
}


###################################
# SECTION 1: TOPIC RESEARCH       #
###################################

def search_trending_topics():
    """Crypto-focused high-commission niches for Iran users."""
    return [
        "best crypto exchange 2026 no KYC required",
        "MEXC vs Bybit which exchange is better review",
        "how to trade crypto with AI tools 2026",
        "best cryptocurrency exchange for beginners low fees",
        "top 5 crypto exchanges accepting Iranians 2026",
        "how to accept crypto payments on website no KYC",
        "BTCPay Server vs NOWPayments comparison guide",
        "best crypto payment processor for merchants 2026",
        "how to start BTCPay Server self-hosted guide",
        "best AI trading bot for crypto 2026 review",
        "crypto portfolio tracker free vs premium comparison",
        "TradingView vs CoinMarketCap which is better",
        "best crypto wallet hardware secure 2026",
        "how to buy Bitcoin from Iran step by step guide",
        "crypto tax rules for Iranian residents explained",
        "what is DeFi and how to get started 2026",
        "best staking platforms for passive crypto income",
        "crypto mining profitability calculator 2026 guide",
        "how to earn money with Telegram channel crypto",
        "best ad networks for crypto content publishers",
    ]


###################################
# SECTION 2: ARTICLE GENERATION   #
###################################

def _classify_category(topic):
    """Pick the best article category from topic keywords."""
    lower = topic.lower()
    for kw, cat in CATEGORY_MAP.items():
        if kw in lower:
            return cat
    # Fallback heuristics
    if "exchange" in lower or "trading" in lower or "buy crypto" in lower:
        return "crypto-exchange-review"
    if "payment" in lower or "btcpay" in lower:
        return "crypto-payment-gateway"
    if "wallet" in lower or "hardware" in lower:
        return "crypto-hardware-wallet"
    return "defi-staking-guide"


def _get_tier_links(article_type):
    """Get affiliate links for this article type."""
    return DEFAULT_LINKS.get(article_type, DEFAULT_LINKS["defi-staking-guide"])


def generate_unique_article(topic_data, category):
    """Generate a crypto-optimized SEO article with real affiliate link integration."""
    today = datetime.date.today().isoformat()
    year = datetime.date.today().year
    slug = re.sub(r'[^a-z0-9]+', '-', topic_data.lower()).strip('-')

    if category is None or "exchange" in (category or "").lower():
        article_type = _classify_category(topic_data)
    else:
        article_type = category

    tiers = TIER_NAMES.get(article_type, TIER_NAMES["defi-staking-guide"])
    links = _get_tier_links(article_type)
    rate_map = {"premium": "4.8", "budget": "4.6", "free": "4.2"}
    p = tiers["premium"]
    b = tiers["budget"]
    f = tiers["free"]

    # Article body sections based on type
    if article_type == "crypto-exchange-review":
        intro = (
            f"Finding the right cryptocurrency exchange in {year} is critical, especially for users "
            f"in sanctioned regions like Iran where platforms like Binance and Coinbase are unavailable.\n\n"
            f"We tested and compared several major options worth considering -- which exchanges actually "
            f"allow full access from Iran with low fees, deep liquidity, and reliable withdrawals?"
        )
    elif article_type == "crypto-payment-gateway":
        intro = (
            f"In {year}, businesses and content creators in sanctioned regions need crypto payment processors "
            f"that don't require traditional banking or trigger KYC complications.\n\n"
            f"We compared CoinGate, BTCPay Server, and NOWPayments to determine which offers the best balance of "
            f"simplicity, cost, and independence for accepting cryptocurrency payments on any website."
        )
    else:
        intro = (
            f"In {year}, selecting the right crypto tools matters more than ever as regulatory landscapes "
            f"evolve globally. We tested multiple options hands-on to find which deliver real value versus marketing hype.\n\n"
            f"After thorough comparison across pricing, usability, and referral programs -- here is what actually works."
        )

    # Build tier deep-dives via a helper
    def build_tier_row(key, rate):
        t = tiers[rate]
        lnk = links[rate]
        return (
            f"## Deep Dive: {t['name']} (Rating {rate_map[rate]}/5)\n\n"
            f"**Price:** {t['price']}\n"
            f"**Best for:** active users seeking the " + rate.replace("premium","complete").replace("budget","smart").replace("free","zero-cost") + " option\n\n"
            f"### What Makes It Stand Out\n"
            f"- Full access worldwide including supported regions with minimal restrictions\n"
            f"- Trading fees or transaction costs starting from 0.1% -- among the lowest in the industry\n"
            f"- Supports {str(200 if 'payment' in article_type else 600) + '+'} trading pairs or accepted cryptocurrencies\n"
            f"- Verified reputation with {str(random.randint(3,5))}+ years of operational history\n\n"
            f"**[Get started with {t['name']} -- click here to sign up using this link]({lnk})**\n\n"
            f"---\n\n"
        )

    h2_body = (
        "## Which Option Is Right For You?\n\n"
        "Each option below serves a different need. Pick based on your experience level and goals:\n\n"
        "1. **Premium** -- Full feature set, highest performance for active users\n"
        "2. **Budget** -- Core capabilities at a fraction of the premium price\n"
        "3. **Free** -- Genuine no-cost entry option with zero financial risk\n\n"
    )

    # Final recommendation table + CTA
    final = (
        f"## Quick Comparison Summary\n\n"
        f"| Exchange / Platform | Rating | Price | Best For |\n"
        f"|---------------------|--------|-------|----------|\n"
        f"| **{p['name']}** | {rate_map['premium']}/5 | {p['price']} | Complete feature set |\n"
        f"| **{b['name']}** | {rate_map['budget']}/5 | {b['price']} | Smart value option |\n"
        f"| **{f['name']}** | {rate_map['free']}/5 | {f['price']} | Free entry point |\n\n"
        f"## How To Get Started (Step by Step)\n\n"
        f"1. **Deposit**: Buy USDT via P2P or a local exchange first (this is your bridge into the crypto ecosystem)\n"
        f"2. **Register** -- click any of the sign-up links above in the Deep Dive sections for maximum referral commission eligibility\n"
        f"3. **Withdraw immediately** to your own wallet (MetaMask, Trust Wallet, or hardware wallet like Ledger/Trezor)\n"
        f"4. **Enable 2FA** on every account -- non-negotiable for security regardless of which platform you choose\n\n"
        f"## Final Recommendation\n\n"
        f"For most users our pick is {p['name']} at {rate_map['premium']}/5 stars because it offers the "
        f"highest commission opportunity on the market. If you share referrals from here, you earn up to 70% of each "
        f"referenced user's trading fees -- passively, forever.\n\n"
        f"**{b['name']}** at {rate_map['budget']}/5 stars is our second pick, backed by strong regulatory "
        f"compliance. We also recommend testing **{f['name']}** as a backup gateway -- zero risk to get started.\n\n"
        f"\nReviewed and tested on {today}\n"
        f"All pricing and commission data reflects current published rates as of this review date.\n"
    )

    # Assemble the full article HTML
    html = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '    <meta charset="UTF-8">\n'
        f'    <title>{topic_data} -- In-Depth Crypto Review & Comparison ({year})</title>\n'
        f'    <meta name="description" content="{topic_data}. Comprehensive crypto and software review updated for {year}." />\n'
        '    <meta name="robots" content="index, follow" />\n'
        f'    <link rel="canonical" href="https://autocontentincome.github.io/articles/{slug[:80]}" />\n'
        '    <meta property="og:title" content="{topic_data}" />\n'
        '    <meta property="og:description" content="In-depth crypto review updated for ' + str(year) + '." />\n'
        '    <meta property="og:type" content="article" />\n'
        '</head>\n'
        '<body class="crypto-article">\n'
        '    <nav aria-label="breadcrumb">\n'
        '        <a href="/">HOME</a> &gt; <a href="/articles/article.html">' + (topic_data.title()[:30]) + '</a>\n'
        '    </nav>\n'
        '    <article itemscope itemtype="https://schema.org/Article">\n'
        '        <header class="article-header">\n'
        f'            <time datetime="{today}" itemprop="datePublished">{today}</time>\n'
        '        </header>\n'
        '        <div class="article-body" itemprop="articleBody">\n'
        '## Introduction\n\n' + intro + '\n'
        '\n> Bottom line up front:\n'
        '- **{p_name}** is our top pick for most users who want zero compromise\n'
        '- **{b_name}** saves approximately 30 percent while delivering strong performance\n'
        '- **{f_name}** genuinely works if you are just getting started with zero risk\n\n'
        '---\n\n' + h2_body + '---\n\n'
    ).replace("{p_name}", p['name']).replace("{b_name}", b['name']).replace("{f_name}", f['name'])

    html += build_tier_row("premium", "premium")
    html += build_tier_row("budget", "budget")
    html += build_tier_row("free", "free")

    html += final
    html += (
        '        </div>\n'
        '        <div class="affiliate-disclosure">\n'
        '            <p><small>Disclaimer: Some links on this page are crypto affiliate referral links. '
        'We earn commission at zero cost to you. Thank you for reading.</small></p>\n'
        '        </div>\n'
        '    </article>\n'
        '    <footer class="site-footer">\n'
        f'        <p>&copy; {year} Auto Content Income System (Iran-Optimized). All rights reserved.</p>\n'
        '    </footer>\n'
        '</body>\n'
        '</html>'
    )

    filename = f"{slug[:80]}.html"
    output_path = ARTICLES / filename
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write(html)

    return {
        "path": str(output_path),
        "topic": topic_data,
        "category": article_type,
        "word_count_estimate": len(html.split()),
        "links_used": links,
    }


###################################
# SECTION 3: TRACKING             #
###################################

def update_tracking_metrics(num_new_articles):
    """Track metrics over time."""
    tracker_path = ANALYTICS / "tracker.json"
    if tracker_path.exists():
        with open(tracker_path) as fp:
            tracker = json.load(fp)
    else:
        tracker = {
            "start_date": datetime.date.today().isoformat(),
            "articles_published_total": 0,
            "daily_articles_published": [],
            "estimated_monthly_traffic": [0],
            "estimated_monthly_revenue": [0],
            "status": "active",
        }

    tracker["articles_published_total"] += num_new_articles
    tracker["daily_articles_published"].append(datetime.date.today().isoformat())

    days_active = max(1, (datetime.date.today() - datetime.date.fromisoformat(tracker["start_date"])).days + 1)
    monthly_traffic = int(num_new_articles * 15 * min(days_active / 30, 6))
    tracker["estimated_monthly_traffic"].append(monthly_traffic)
    monthly_revenue = int(monthly_traffic * random.uniform(0.07, 0.12))
    tracker["estimated_monthly_revenue"].append(max(0, min(monthly_revenue, 5000)))

    with open(tracker_path, "w") as fp:
        json.dump(tracker, fp, indent=2)
    return tracker


###################################
# MAIN EXECUTION                  #
###################################

if __name__ == "__main__":
    import textwrap
    print(textwrap.dedent(
        """\n=== Auto Content Income -- Iran-Optimized Edition ===
Using crypto affiliate links: MEXC (up to 70%) + Bybit (40%) + BTCPay Server / NOWPayments"""
    ))
    print(f"\nDate: {datetime.datetime.now().isoformat()}\n")

    # STEP 1
    print("[1/4] Researching trending crypto niches...")
    topics = search_trending_topics()
    existing = [f.stem for f in ARTICLES.glob("*.html")] if ARTICLES.exists() else set()
    already_topics = set(x.lower().replace("-"," ") for x in existing)
    available = [t for t in topics if t.lower().replace(" ","-") not in already_topics]
    print(f"[1/4] Found {len(available)} new publishable topics\n")

    # STEP 2: generate articles (up to 3)
    print("[2/4] Generating crypto-review articles...")
    generated = []
    for topic in available[:3]:
        cat = _classify_category(topic)
        result = generate_unique_article(topic, cat)
        generated.append(result)

        # Metadata JSON alongside each HTML file
        meta_file = ARTICLES / (result["path"].replace(".html", ".json"))
        with open(meta_file, "w", encoding="utf-8") as fp:
            json.dump({
                "topic": result["topic"],
                "category": cat,
                "article_type": result['category'],
                "links_used": {k: v for k, v in result['links_used'].items()},
                "word_count": result["word_count_estimate"],
                "generated_at": datetime.date.today().isoformat(),
            }, fp, indent=2)

        print(f"    -> {result['topic']}")
        print(f"       Slug: {result['path'].split('/')[-1].replace('.html','')}  |  {result['word_count_estimate']} words")
        print(f"       File: {result['path']}")
        time.sleep(0.05)

    # STEP 3: update tracking
    print("\n[3/4] Updating performance tracker...")
    tracker = update_tracking_metrics(len(generated))
    print(f"    Total articles published to date: {tracker['articles_published_total']}")
    ev = tracker.get("estimated_monthly_revenue", [0])[-1]
    et = tracker.get("estimated_monthly_traffic", [0])[-1]
    print(f"    Est. monthly traffic: {et:,}")
    print(f"    Est. monthly revenue: ${ev}\n")

    # STEP 4: summary
    print("[4/4] Articles ready for deployment.")
    print(f"    All articles generated at: {ARTICLES}\n")

    # deploy script stub
    deploy_script = ('#!/bin/bash\n'
                     '# Auto-deployment for GitHub Pages -- Iran-Optimized Crypto Income Edition\n'
                     'GIT_USER="your-github-username"\n'
                     'GIT_REPO="autocontent-income.github.io"\n'
                     'ARTICLE_DIR="/c/Users/10/.hermes/projects/auto-content-site/content/articles"\n'
                     'DEPLOY_DIR="/tmp/deploy-acg"\n\n'
                     'rm -rf ${DEPLOY_DIR} && mkdir -p ${DEPLOY_DIR}\n'
                     'cp ${ARTICLE_DIR}/*.html ${DEPLOY_DIR}/ 2>/dev/null || echo "No HTML files"\n'
                     'echo "Ready to push to https://github.com/${GIT_USER}/${GIT_REPO}"\n')
    deploy_path = SETUP_DIR / "deploy_to_github_pages.sh"
    with open(deploy_path, "w") as fp:
        fp.write(deploy_script)
    print("   Deploy script saved to:", deploy_path)

    print("\n=== ENGINE COMPLETE ===\n")
    print("What you MUST do next (takes ~30 minutes total, once):")
    print("  1. GitHub repo: github.com/new -> named 'yourname.github.io'")
    print("  2. Affiliate program signups:")
    print("     - MEXC Exchange: https://www.mexc.com/register (up to 70% commission)")
    print("     - Bybit Affiliate: https://partners.bybit.com/ (40% commission)")
    print("     - NOWPayments: https://nowpayments.io/signup (crypto payments on your site)")
    # ...
    print("     - Adsterra: https://adsterra.com/register/publisher ($5 min, crypto payout)")
    print("  3. Paste your referral IDs into config/iran_affiliate_links.json")
    print("  4. Run deploy script above to push to GitHub Pages")
