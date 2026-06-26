#!/usr/bin/env python3
"""
Automated content generator for VMDProjects.github.io
Generates SEO-optimized articles with crypto/fintech affiliate links
"""

import json
import os
from datetime import datetime, timedelta
import hashlib
import random

# Configuration
ARTICLE_COUNT = 3  # Generate 3 new articles per day
OUTPUT_DIR = "articles"
CONFIG_FILE = "config/affiliates.json"
LOG_FILE = "logs/generation.log"
GENERATED_TRACKER = "logs/generated_articles.json"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def log_message(message):
    """Write message to log file and print to console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def load_config():
    """Load affiliate configuration"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        log_message(f"Error loading config: {e}")
    
    # Default config if file doesn't exist
    return {
        "nowpayments": {
            "referral_link": "https://account.nowpayments.io/create-account?link_id=2996241443",
            "merchant_id": "NOW_MERCHANT_ID"
        },
        "adsterra": {
            "pop_unders": '<script src="https://pl29901420.effectivecpmnetwork.com/96/46/60/96466007a40f0c546818a7b528b43400.js"></script>',
            "direct_link": "https://www.effectivecpmnetwork.com/h0niswc1?key=59036b18a53b13a875c7706d579f9e92"
        }
    }

def generate_article_slug(title):
    """Generate URL-friendly slug from title"""
    slug = title.lower().replace(" ", "-").replace("?", "").replace("!", "")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    return slug

def get_previously_generated():
    """Load list of previously generated articles to avoid duplicates"""
    if os.path.exists(GENERATED_TRACKER):
        try:
            with open(GENERATED_TRACKER, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_generated_article(title, slug):
    """Track generated articles"""
    articles = get_previously_generated()
    articles.append({
        "title": title,
        "slug": slug,
        "generated_date": datetime.now().isoformat()
    })
    with open(GENERATED_TRACKER, "w") as f:
        json.dump(articles, f, indent=2)

def generate_html_article(title, content_html, config, slug, topic):
    """Generate complete HTML article with affiliate links and ads"""
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # Extract affiliate links
    nowpay_link = config["nowpayments"]["referral_link"]
    adsterra_pops = config["adsterra"]["pop_unders"]
    adsterra_direct = config["adsterra"]["direct_link"]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - Comprehensive guide to {topic}. Learn best practices and strategies.">
    <meta name="keywords" content="{topic}, crypto, blockchain, trading, guide, tutorial">
    <meta name="author" content="VMDProjects">
    <meta name="date" content="{date_str}">
    
    <!-- Open Graph Tags for Social Sharing -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="Expert guide on {topic}">
    <meta property="og:url" content="https://vmdprojects.github.io/articles/{slug}.html">
    <meta property="og:image" content="https://vmdprojects.github.io/assets/og-image.jpg">
    
    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "datePublished": "{date_str}",
        "author": {{
            "@type": "Organization",
            "name": "VMDProjects"
        }},
        "image": "https://vmdprojects.github.io/assets/og-image.jpg"
    }}
    </script>
    
    <title>{title} | VMDProjects</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
            border-bottom: 2px solid #eee;
            padding-bottom: 15px;
        }}
        
        h2 {{
            color: #764ba2;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .affiliate-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            margin: 30px 0;
            text-align: center;
        }}
        
        .affiliate-box h3 {{
            color: white;
            margin-bottom: 15px;
        }}
        
        .affiliate-box a {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 12px 30px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px 5px;
            transition: transform 0.3s;
        }}
        
        .affiliate-box a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .content {{
            line-height: 1.8;
        }}
        
        .content ul, .content ol {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        
        .content li {{
            margin-bottom: 8px;
        }}
        
        .cta-banner {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 30px 0;
            border-radius: 5px;
        }}
        
        .back-link {{
            display: inline-block;
            margin-top: 30px;
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
            text-align: center;
        }}
        
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="meta">
            Published: {date_str} | Reading time: ~{random.randint(3,8)} min
        </div>
        
        <div class="content">
            {content_html}
        </div>
        
        <!-- Affiliate Call-to-Action -->
        <div class="affiliate-box">
            <h3>Start Your Crypto Journey Today</h3>
            <p>Join thousands of users managing their crypto payments securely</p>
            <a href="{nowpay_link}" target="_blank" rel="noopener noreferrer">Join NOWPayments →</a>
        </div>
        
        <!-- Important Disclaimer -->
        <div class="disclaimer">
            <strong>Disclaimer:</strong> This article is for educational purposes only. Cryptocurrency and trading involve risk of loss. Past performance does not guarantee future results. Always do your own research (DYOR) and never invest more than you can afford to lose.
        </div>
        
        <footer>
            <p>&copy; 2024 VMDProjects. All rights reserved.</p>
            <p><a href="https://vmdprojects.github.io" style="color: #667eea; text-decoration: none;">← Back to Home</a></p>
        </footer>
    </div>
    
    <!-- Adsterra PopUnders Ad Code -->
    {adsterra_pops}
</body>
</html>"""
    
    return html

def generate_article_topics():
    """Generate diverse article topics for better SEO coverage"""
    topics = [
        {
            "title": "How to Accept Cryptocurrency Payments in 2024: Complete Guide",
            "topic": "cryptocurrency payments",
            "slug": "accept-crypto-payments-2024"
        },
        {
            "title": "Bitcoin vs Ethereum: Detailed Comparison for Beginners",
            "topic": "bitcoin ethereum comparison",
            "slug": "bitcoin-vs-ethereum-guide"
        },
        {
            "title": "Decentralized Finance (DeFi) Explained: A Beginner's Guide",
            "topic": "decentralized finance DeFi",
            "slug": "defi-guide-beginners"
        },
        {
            "title": "How to Secure Your Crypto Wallet: Best Practices 2024",
            "topic": "crypto wallet security",
            "slug": "secure-crypto-wallet"
        },
        {
            "title": "Blockchain Technology Explained: From Basics to Applications",
            "topic": "blockchain technology",
            "slug": "blockchain-technology-guide"
        },
        {
            "title": "Trading Cryptocurrency: Strategies for Beginners and Pros",
            "topic": "crypto trading strategies",
            "slug": "crypto-trading-strategies"
        },
        {
            "title": "NFTs Explained: Understanding Digital Assets and Ownership",
            "topic": "NFT digital assets",
            "slug": "nft-guide-explained"
        },
        {
            "title": "Staking Cryptocurrency: Earn Passive Income on Your Holdings",
            "topic": "crypto staking passive income",
            "slug": "crypto-staking-guide"
        },
        {
            "title": "The Future of Crypto: Trends and Predictions for 2025",
            "topic": "crypto trends future",
            "slug": "crypto-trends-2025"
        },
        {
            "title": "Smart Contracts: Revolutionizing Digital Agreements",
            "topic": "smart contracts blockchain",
            "slug": "smart-contracts-guide"
        }
    ]
    return topics

def generate_article_content(title, topic):
    """Generate SEO-optimized article content"""
    
    content_templates = {
        "How to Accept Cryptocurrency Payments": """
            <h2>Why Accept Cryptocurrency Payments?</h2>
            <p>In today's digital economy, accepting cryptocurrency payments offers numerous advantages for businesses of all sizes. From reduced transaction fees to instant settlement, crypto payments are revolutionizing how businesses handle transactions globally.</p>
            
            <h2>Key Benefits</h2>
            <ul>
                <li><strong>Lower Fees:</strong> Cryptocurrency transactions typically have lower fees compared to traditional payment methods like credit cards (2-3% instead of 3-4%)</li>
                <li><strong>Instant Settlements:</strong> Transactions are processed in minutes, not days</li>
                <li><strong>Global Reach:</strong> Accept payments from customers anywhere in the world</li>
                <li><strong>Reduced Chargebacks:</strong> Crypto transactions are irreversible, eliminating chargeback fraud</li>
                <li><strong>Enhanced Security:</strong> Blockchain technology provides unparalleled security</li>
            </ul>
            
            <h2>How to Get Started</h2>
            <p>The process of accepting cryptocurrency payments is simpler than ever. You don't need technical expertise or complex infrastructure setup. Modern payment gateways have democratized access to crypto payments for businesses of all sizes.</p>
            
            <h2>Popular Cryptocurrencies to Accept</h2>
            <p>Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC), and stablecoins like USDT and USDC are the most popular choices. Each offers different advantages depending on your business model.</p>
            
            <h2>Step-by-Step Implementation</h2>
            <ol>
                <li>Choose a payment processor that supports your desired cryptocurrencies</li>
                <li>Create a merchant account and verify your identity</li>
                <li>Integrate the payment gateway into your website</li>
                <li>Test transactions thoroughly before going live</li>
                <li>Monitor and manage your crypto holdings</li>
            </ol>
            
            <h2>Security Considerations</h2>
            <p>When accepting crypto payments, security is paramount. Use reputable payment processors with insurance coverage, enable two-factor authentication, and regularly audit your transactions.</p>
        """,
        
        "Bitcoin vs Ethereum": """
            <h2>Understanding the Differences</h2>
            <p>Bitcoin and Ethereum are the two largest cryptocurrencies by market capitalization, but they serve different purposes on the blockchain network. Understanding their differences is crucial for investors and enthusiasts.</p>
            
            <h2>Bitcoin: Digital Gold</h2>
            <p>Bitcoin was created in 2009 as a peer-to-peer electronic cash system. Its primary function is to serve as a store of value and medium of exchange. With a fixed supply of 21 million coins, Bitcoin's scarcity makes it valuable.</p>
            
            <h2>Ethereum: The Smart Contract Platform</h2>
            <p>Ethereum, launched in 2015, introduced smart contracts - self-executing programs on the blockchain. This innovation enabled developers to build decentralized applications (dApps) on the Ethereum network.</p>
            
            <h2>Key Differences Table</h2>
            <ul>
                <li><strong>Purpose:</strong> Bitcoin is a currency; Ethereum is a platform</li>
                <li><strong>Supply:</strong> Bitcoin has 21 million cap; Ethereum is unlimited</li>
                <li><strong>Block Time:</strong> Bitcoin takes ~10 minutes; Ethereum takes ~12 seconds</li>
                <li><strong>Use Cases:</strong> Bitcoin for payments; Ethereum for dApps and DeFi</li>
            </ul>
            
            <h2>Investment Considerations</h2>
            <p>Both assets carry different risk profiles. Bitcoin is seen as more stable due to its fixed supply, while Ethereum offers exposure to the growing DeFi ecosystem.</p>
            
            <h2>Which Should You Choose?</h2>
            <p>The answer depends on your investment goals. Bitcoin suits those seeking a long-term store of value, while Ethereum appeals to those interested in blockchain applications and DeFi opportunities.</p>
        """,
        
        "DeFi Explained": """
            <h2>What is Decentralized Finance?</h2>
            <p>Decentralized Finance (DeFi) refers to financial services built on blockchain networks, eliminating intermediaries like banks. DeFi protocols offer lending, borrowing, trading, and yield farming opportunities directly to users.</p>
            
            <h2>How DeFi Works</h2>
            <p>DeFi operates through smart contracts - programmable agreements that execute automatically when conditions are met. No middleman, no waiting periods, just pure peer-to-peer finance.</p>
            
            <h2>Core DeFi Services</h2>
            <ul>
                <li><strong>Lending & Borrowing:</strong> Earn interest by lending crypto or borrow against collateral</li>
                <li><strong>Decentralized Exchanges:</strong> Trade directly from your wallet without intermediaries</li>
                <li><strong>Yield Farming:</strong> Earn returns by providing liquidity to protocols</li>
                <li><strong>Staking:</strong> Earn rewards by securing the network</li>
            </ul>
            
            <h2>Advantages of DeFi</h2>
            <p>DeFi offers 24/7 access, transparent pricing, lower fees, and financial inclusion for anyone with internet access. There are no banking hours or geographical restrictions.</p>
            
            <h2>Risks to Consider</h2>
            <p>DeFi is still emerging technology. Smart contract bugs, market volatility, and regulatory uncertainty present risks. Always research thoroughly before investing.</p>
            
            <h2>The Future of Finance</h2>
            <p>DeFi is reshaping how people think about money and financial services. As the ecosystem matures and regulation becomes clearer, adoption will likely accelerate significantly.</p>
        """
    }
    
    # Match template to topic or use default
    for key, template in content_templates.items():
        if key.lower() in title.lower():
            return template
    
    # Default content if no specific template
    return f"""
        <h2>Introduction to {topic}</h2>
        <p>This comprehensive guide covers everything you need to know about {topic}. Whether you're a beginner or experienced investor, understanding these concepts is crucial for success in the cryptocurrency space.</p>
        
        <h2>Key Concepts</h2>
        <ul>
            <li>Understanding blockchain fundamentals</li>
            <li>Market dynamics and trading basics</li>
            <li>Risk management strategies</li>
            <li>Security best practices</li>
            <li>Future opportunities and trends</li>
        </ul>
        
        <h2>Getting Started</h2>
        <p>The cryptocurrency market is accessible to everyone. Start with small investments, educate yourself continuously, and never invest money you can't afford to lose.</p>
        
        <h2>Conclusion</h2>
        <p>{topic.title()} represents an important part of the modern financial landscape. Understanding its nuances will help you make informed decisions in your financial journey.</p>
    """

def main():
    """Main function to orchestrate content generation"""
    log_message("=" * 60)
    log_message("Starting content generation process")
    log_message("=" * 60)
    
    config = load_config()
    log_message(f"✓ Configuration loaded")
    
    previously_generated = get_previously_generated()
    log_message(f"✓ Found {len(previously_generated)} previously generated articles")
    
    topics = generate_article_topics()
    generated_count = 0
    
    # Select random topics to generate
    selected_topics = random.sample(topics, min(ARTICLE_COUNT, len(topics)))
    
    for topic_data in selected_topics:
        title = topic_data["title"]
        topic = topic_data["topic"]
        slug = topic_data["slug"]
        
        # Check if already generated
        if any(art["slug"] == slug for art in previously_generated):
            log_message(f"⊘ Skipping {slug} (already generated)")
            continue
        
        try:
            # Generate content
            content = generate_article_content(title, topic)
            
            # Generate HTML
            html = generate_html_article(title, content, config, slug, topic)
            
            # Save to file
            output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            
            # Track generated article
            save_generated_article(title, slug)
            
            log_message(f"✓ Generated: {title}")
            log_message(f"  └─ Saved to: {output_path}")
            generated_count += 1
            
        except Exception as e:
            log_message(f"✗ Error generating {title}: {e}")
    
    log_message("=" * 60)
    log_message(f"Generation complete: {generated_count} new articles created")
    log_message("=" * 60)
    
    return generated_count > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
