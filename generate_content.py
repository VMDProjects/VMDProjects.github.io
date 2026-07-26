#!/usr/bin/env python3
"""
VMDProjects Automated Content Generator
Generates SEO-optimized cryptocurrency and fintech articles with affiliate links
Production-ready for GitHub Actions automation
"""

import json
import os
from datetime import datetime, timedelta
import hashlib
import random
from pathlib import Path

# ============================================================
# CONFIGURATION - YOUR AFFILIATE LINKS
# ============================================================
ARTICLE_COUNT = 3  # Generate 3 new articles per day
OUTPUT_DIR = "articles"  # Local articles directory
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
    """Load affiliate configuration from config file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        log_message(f"Error loading config: {e}")
    
    # Default config if file doesn't exist
    return {
        "nowpayments": {
            "referral_link": "https://account.nowpayments.io/create-account?link_id=2996241443"
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
        }}
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
        
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
            text-align: center;
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
    """
    Generate 5000+ unique article topics programmatically.

    Rather than hand-writing thousands of titles, this combines a large
    pool of SUBJECTS (coins, protocols, concepts) with a large pool of
    ANGLE_TEMPLATES (title formats). Every subject x angle combination
    produces a distinct title/topic/slug, so the pool scales to
    len(SUBJECTS) * len(ANGLE_TEMPLATES) unique topics with zero
    duplicate slugs.
    """

    SUBJECTS = [
        # Major coins
        "Bitcoin", "Ethereum", "Litecoin", "Ripple (XRP)", "Cardano", "Solana",
        "Polkadot", "Dogecoin", "Monero", "Chainlink", "Polygon", "Avalanche",
        "Cosmos", "Algorand", "Stellar", "Tezos", "VeChain", "Hedera",
        "Near Protocol", "Aptos", "Sui", "Toncoin", "Tron", "EOS",
        "Bitcoin Cash", "Filecoin", "The Graph", "Fantom", "Injective",
        "Sei Network", "Celestia", "Mantle", "Blast", "Kaspa",
        "Shiba Inu", "Meme Coins", "Pepe Coin", "Internet Computer", "Kaspa Mining",
        # Layer 2 / scaling
        "Arbitrum", "Optimism", "Base", "zkSync", "StarkNet", "Layer 2 Rollups",
        "ZK-Rollups", "Optimistic Rollups", "Sidechains", "State Channels",
        "Modular Blockchains", "Rollup-as-a-Service", "Data Availability Layers",
        # Stablecoins & payments
        "Stablecoins", "USDT (Tether)", "USDC", "DAI", "Algorithmic Stablecoins",
        "Cryptocurrency Payment Gateways", "NOWPayments", "Crypto Debit Cards",
        "Cross-Border Crypto Payments", "Remittances via Crypto", "Merchant Crypto Adoption",
        # DeFi
        "Decentralized Finance (DeFi)", "Uniswap", "Aave", "Compound Finance",
        "Curve Finance", "MakerDAO", "Yearn Finance", "Liquidity Pools",
        "Yield Farming", "Flash Loans", "Impermanent Loss", "Decentralized Exchanges (DEXs)",
        "Automated Market Makers", "Lending Protocols", "Synthetic Assets",
        "Decentralized Derivatives", "DeFi Insurance", "Real World Asset Tokenization",
        "Perpetual Futures Protocols", "DeFi Aggregators", "Cross-Chain DeFi",
        "Restaking", "Liquid Restaking Tokens", "Real Yield in DeFi",
        # Wallets & security
        "Hardware Wallets", "Hot Wallets", "Cold Storage", "Multi-Signature Wallets",
        "Seed Phrases", "Private Key Management", "Crypto Wallet Recovery",
        "Two-Factor Authentication for Crypto", "Crypto Phishing Scams",
        "Smart Contract Audits", "Self-Custody", "Ledger Hardware Wallets",
        "Trezor Hardware Wallets", "Crypto Insurance", "MetaMask", "Trust Wallet",
        "Coinbase Wallet", "Air-Gapped Wallets", "Social Recovery Wallets",
        "Crypto Estate Planning",
        # Trading & investing
        "Cryptocurrency Trading", "Technical Analysis", "Crypto Risk Management",
        "Day Trading Crypto", "Swing Trading Crypto", "Leverage Trading",
        "Spot Trading", "Futures Trading", "Crypto Portfolio Diversification",
        "Dollar Cost Averaging", "On-Chain Analysis", "Whale Watching",
        "Crypto Market Cycles", "HODLing", "Crypto Fundamental Analysis",
        "Altcoin Investing", "Crypto Exchange Comparison", "Order Book Trading",
        "Options Trading in Crypto", "Copy Trading", "Algorithmic Crypto Trading",
        "Crypto Trading Bots", "Arbitrage Trading", "Market Making Strategies",
        # Blockchain concepts
        "Blockchain Technology", "Smart Contracts", "Proof of Work",
        "Proof of Stake", "Consensus Mechanisms", "Blockchain Oracles",
        "Cross-Chain Bridges", "Blockchain Interoperability", "Blockchain Forks",
        "Sharding", "Decentralized Autonomous Organizations (DAOs)",
        "Decentralized Identity", "Blockchain Scalability", "Blockchain Governance",
        "Account Abstraction", "Zero-Knowledge Proofs",
        # NFTs & digital assets
        "NFTs (Non-Fungible Tokens)", "NFT Marketplaces", "NFT Gaming",
        "Digital Art and NFTs", "NFT Royalties", "Soulbound Tokens",
        # Mining & staking
        "Cryptocurrency Mining", "Bitcoin Mining", "Crypto Staking",
        "Liquid Staking", "Mining Pools", "Cloud Mining", "Proof of Stake Validators",
        # Regulation & macro
        "Cryptocurrency Regulation", "Crypto Taxes", "Central Bank Digital Currencies (CBDCs)",
        "Crypto AML/KYC Compliance", "SEC and Crypto Regulation",
        "Institutional Crypto Adoption", "Crypto ETFs", "Bitcoin Halving",
        "MiCA Regulation in Europe", "Crypto Regulation in the United States",
        "Crypto Regulation in Asia", "FATF Travel Rule", "Crypto Custody Regulations",
        "Bitcoin ETFs", "Ethereum ETFs", "Crypto Index Funds",
        # Emerging & niche
        "Web3", "The Metaverse", "GameFi (Play-to-Earn)", "Social Tokens",
        "AI and Cryptocurrency", "Decentralized Physical Infrastructure (DePIN)",
        "Green and Sustainable Crypto Mining", "Quantum Computing and Cryptography",
        "Privacy Coins", "Crypto Lending Platforms", "Crypto Savings Accounts",
        "Tokenized Real Estate", "Supply Chain on Blockchain", "Crypto in Gaming",
        "Crypto for Freelancers", "Crypto Remittances in Emerging Markets",
        "Decentralized Storage", "Decentralized Social Media",
        "Tokenized Carbon Credits", "Crypto Philanthropy", "Crypto for the Unbanked",
        "Blockchain in Healthcare", "Blockchain in Voting Systems",
        "Blockchain in Education", "Decentralized Science (DeSci)",
    ]

    ANGLE_TEMPLATES = [
        "{subject}: A Complete Guide for 2025",
        "How Does {subject} Work? Explained Simply",
        "{subject} vs Traditional Finance: Key Differences",
        "Top 10 Things to Know About {subject}",
        "Is {subject} Safe? A Security Analysis",
        "{subject} for Beginners: Step-by-Step Guide",
        "The Pros and Cons of {subject}",
        "{subject} in 2025: Trends and Predictions",
        "How to Get Started with {subject} Today",
        "{subject} Explained: Everything You Need to Know",
        "Common Mistakes to Avoid When Using {subject}",
        "{subject} Tax Implications: What You Should Know",
        "Is {subject} a Good Investment in 2025?",
        "{subject} vs Competitors: An Honest Comparison",
        "The Ultimate {subject} Resource Guide",
        "{subject} Security Best Practices",
        "How {subject} Is Changing the Financial Industry",
        "{subject} Fees Explained: What You're Really Paying",
        "Building Passive Income with {subject}",
        "{subject} Regulations: A Global Overview",
        "The History and Evolution of {subject}",
        "{subject} Use Cases Beyond Speculation",
        "Advanced {subject} Strategies for Experienced Users",
        "{subject} Risks: What Nobody Tells You",
        "How Institutions Are Adopting {subject}",
        "{subject} Myths Debunked",
        "A Beginner's Roadmap to {subject}",
        "{subject} Adoption in Emerging Markets",
        "The Environmental Impact of {subject}",
        "{subject} and the Future of Payments",
        "Is Now the Time to Get Into {subject}?",
        "{subject} Community and Ecosystem Overview",
        "What Experts Are Saying About {subject} in 2025",
        "{subject} for Small Businesses: A Practical Guide",
        "Frequently Asked Questions About {subject}",
        "{subject}: Long-Term Outlook and Predictions",
        "How to Evaluate {subject} Before Investing",
        "{subject} and Financial Inclusion",
        "The Biggest Misconceptions About {subject}",
        "{subject} Case Studies: Real-World Examples",
        "{subject} Explained in Plain English",
        "5 Reasons to Pay Attention to {subject}",
        "{subject}: Opportunities and Challenges Ahead",
        "How to Research {subject} Like a Pro",
        "{subject} Terminology Every Beginner Should Know",
        "The Real Cost of Using {subject}",
        "{subject} Compliance Checklist for 2025",
        "Why {subject} Matters for Everyday Investors",
        "{subject} Red Flags to Watch Out For",
        "Building a Career Around {subject}",
        "{subject}: What Changed in the Last Year",
        "A Skeptic's Guide to {subject}",
        "{subject} Success Stories and Lessons Learned",
        "How Governments Are Responding to {subject}",
        "{subject} Explained Through Real Examples",
        "Is {subject} Overhyped? A Balanced Look",
        "{subject} Integration Guide for Developers",
        "{subject}: What the Data Actually Shows",
        "Preparing for the Next Phase of {subject}",
        "{subject} Glossary: Key Terms Defined",
        "How {subject} Compares Across Regions",
        "{subject} and Retirement Planning",
        "The Hidden Risks of Ignoring {subject}",
        "{subject} Roadmap: What's Coming Next",
        "Getting Expert-Level Knowledge of {subject}",
    ]

    def slugify(text):
        slug = text.lower()
        # Keep only alphanumerics and spaces, everything else becomes a space
        slug = "".join(c if c.isalnum() else " " for c in slug)
        slug = "-".join(slug.split())
        return slug[:80]

    topics = []
    seen_slugs = set()

    for subject in SUBJECTS:
        for template in ANGLE_TEMPLATES:
            title = template.format(subject=subject)
            slug = slugify(title)

            # Guarantee uniqueness even in rare collision cases
            base_slug = slug
            suffix = 2
            while slug in seen_slugs:
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            seen_slugs.add(slug)

            topics.append({
                "title": title,
                "topic": subject.lower(),
                "slug": slug,
            })

    return topics


def _legacy_hardcoded_topics_reference():
    """
    Retained for reference only - no longer used. The original hand-written
    10-topic (later 75-topic) list has been replaced by the programmatic
    generator above, which produces 5000+ unique topics automatically.
    """
    topics = [
        # Cryptocurrency Basics (10)
        {"title": "How to Accept Cryptocurrency Payments in 2024: Complete Guide", "topic": "cryptocurrency payments", "slug": "accept-crypto-payments-2024"},
        {"title": "Bitcoin vs Ethereum: Detailed Comparison for Beginners", "topic": "bitcoin ethereum comparison", "slug": "bitcoin-vs-ethereum-guide"},
        {"title": "Decentralized Finance (DeFi) Explained: A Beginner's Guide", "topic": "decentralized finance DeFi", "slug": "defi-guide-beginners"},
        {"title": "How to Secure Your Crypto Wallet: Best Practices 2024", "topic": "crypto wallet security", "slug": "secure-crypto-wallet"},
        {"title": "Blockchain Technology Explained: From Basics to Applications", "topic": "blockchain technology", "slug": "blockchain-technology-guide"},
        {"title": "Trading Cryptocurrency: Strategies for Beginners and Pros", "topic": "crypto trading strategies", "slug": "crypto-trading-strategies"},
        {"title": "NFTs Explained: Understanding Digital Assets and Ownership", "topic": "NFT digital assets", "slug": "nft-guide-explained"},
        {"title": "Staking Cryptocurrency: Earn Passive Income on Your Holdings", "topic": "crypto staking passive income", "slug": "crypto-staking-guide"},
        {"title": "The Future of Crypto: Trends and Predictions for 2025", "topic": "crypto trends future", "slug": "crypto-trends-2025"},
        {"title": "Smart Contracts: Revolutionizing Digital Agreements", "topic": "smart contracts blockchain", "slug": "smart-contracts-guide"},
        
        # Payment Processors (10)
        {"title": "NOWPayments vs Traditional Payment Gateways: Complete Comparison", "topic": "payment processor comparison", "slug": "nowpayments-vs-traditional"},
        {"title": "How to Set Up Crypto Payments for Your E-commerce Business", "topic": "crypto ecommerce payments", "slug": "ecommerce-crypto-setup"},
        {"title": "Instant Cryptocurrency Settlements: Why Speed Matters", "topic": "instant crypto settlement", "slug": "instant-crypto-settlement"},
        {"title": "Zero Fee Crypto Payments: Myth or Reality?", "topic": "zero fee crypto payments", "slug": "zero-fee-crypto-payments"},
        {"title": "Multi-Currency Payment Processing with Crypto", "topic": "multi-currency payments", "slug": "multi-currency-crypto-payments"},
        {"title": "Webhook Integration Guide for Crypto Payments", "topic": "crypto webhooks integration", "slug": "crypto-webhooks-guide"},
        {"title": "Invoice Management in Cryptocurrency: Best Practices", "topic": "crypto invoicing", "slug": "crypto-invoice-management"},
        {"title": "Stablecoin Payments: The Bridge Between Crypto and Fiat", "topic": "stablecoin payments", "slug": "stablecoin-payments-guide"},
        {"title": "Merchant Tools for Cryptocurrency Adoption", "topic": "merchant crypto tools", "slug": "merchant-crypto-tools"},
        {"title": "API Integration for Crypto Payments: Developer Guide", "topic": "crypto payment API", "slug": "crypto-payment-api-guide"},
        
        # Trading & Exchanges (10)
        {"title": "Cryptocurrency Exchange Comparison 2024: Fees, Features, Security", "topic": "crypto exchange comparison", "slug": "crypto-exchange-comparison"},
        {"title": "How to Trade Altcoins: A Complete Strategy Guide", "topic": "altcoin trading", "slug": "altcoin-trading-guide"},
        {"title": "Technical Analysis for Crypto Trading: Indicators That Work", "topic": "crypto technical analysis", "slug": "crypto-technical-analysis"},
        {"title": "Risk Management in Crypto Trading: Protect Your Portfolio", "topic": "crypto risk management", "slug": "crypto-risk-management"},
        {"title": "Day Trading vs Swing Trading Cryptocurrencies", "topic": "day trading crypto", "slug": "day-trading-vs-swing-trading"},
        {"title": "Leverage Trading in Crypto: How It Works and the Risks", "topic": "crypto leverage trading", "slug": "crypto-leverage-trading"},
        {"title": "Spot Trading vs Futures: Which Is Right for You?", "topic": "spot vs futures trading", "slug": "spot-vs-futures-guide"},
        {"title": "Liquidity Pools and Yield Farming: Earn While You Trade", "topic": "liquidity pools yield farming", "slug": "liquidity-pools-guide"},
        {"title": "Moon Coins vs Established Cryptocurrencies: Investment Strategy", "topic": "altcoin investment", "slug": "moon-coins-strategy"},
        {"title": "How to Read Crypto Charts Like a Professional Trader", "topic": "crypto chart analysis", "slug": "crypto-chart-analysis"},
        
        # Blockchain & Web3 (10)
        {"title": "Ethereum 2.0: What Changed and Why It Matters", "topic": "Ethereum 2.0", "slug": "ethereum-2-guide"},
        {"title": "Layer 2 Scaling Solutions: Faster, Cheaper Transactions", "topic": "layer 2 blockchain", "slug": "layer-2-scaling-guide"},
        {"title": "Web3 Explained: The Future of the Internet", "topic": "Web3 future internet", "slug": "web3-explained-guide"},
        {"title": "Solana vs Ethereum: Which Blockchain Will Win?", "topic": "solana ethereum comparison", "slug": "solana-vs-ethereum"},
        {"title": "Polkadot Ecosystem: Multi-Chain Future Explained", "topic": "polkadot ecosystem", "slug": "polkadot-ecosystem-guide"},
        {"title": "Proof of Work vs Proof of Stake: Understanding Consensus", "topic": "proof of work stake", "slug": "pow-vs-pos-guide"},
        {"title": "Cross-Chain Bridges: Connecting Blockchain Networks", "topic": "cross-chain bridges", "slug": "cross-chain-bridges-guide"},
        {"title": "Cryptocurrency Forks Explained: Hard Forks and Soft Forks", "topic": "crypto forks", "slug": "crypto-forks-guide"},
        {"title": "Blockchain Oracles: Connecting Real-World Data to Smart Contracts", "topic": "blockchain oracles", "slug": "blockchain-oracles-guide"},
        {"title": "Interoperability in Crypto: The Missing Piece", "topic": "crypto interoperability", "slug": "crypto-interoperability-guide"},
        
        # Security & Wallets (10)
        {"title": "Hardware Wallets vs Hot Wallets: Complete Security Guide", "topic": "hardware vs hot wallets", "slug": "hardware-vs-hot-wallets"},
        {"title": "How to Recover Your Lost Cryptocurrency Wallet", "topic": "crypto wallet recovery", "slug": "crypto-wallet-recovery"},
        {"title": "Multi-Signature Wallets: The Ultimate Security Solution", "topic": "multi-sig wallets", "slug": "multi-sig-wallets-guide"},
        {"title": "Crypto Phishing Attacks: How to Protect Yourself", "topic": "crypto phishing protection", "slug": "crypto-phishing-protection"},
        {"title": "Self-Custody vs Exchange Custody: Which Is Safer?", "topic": "self-custody cryptocurrency", "slug": "self-custody-guide"},
        {"title": "Private Keys and Seed Phrases: Never Lose Your Crypto Again", "topic": "crypto seed phrases", "slug": "seed-phrases-guide"},
        {"title": "Two-Factor Authentication for Crypto: Best Practices", "topic": "2FA crypto security", "slug": "2fa-crypto-guide"},
        {"title": "Ledger vs Trezor: Hardware Wallet Comparison", "topic": "ledger trezor comparison", "slug": "ledger-vs-trezor"},
        {"title": "Cold Storage for Crypto: The Most Secure Method", "topic": "cold storage cryptocurrency", "slug": "cold-storage-guide"},
        {"title": "Escrow Services in Cryptocurrency: How They Work", "topic": "crypto escrow", "slug": "crypto-escrow-guide"},
        
        # DeFi Deep Dive (10)
        {"title": "Uniswap Guide: Decentralized Exchange Tutorial", "topic": "Uniswap DEX", "slug": "uniswap-guide"},
        {"title": "Aave Protocol: Lending and Borrowing Explained", "topic": "Aave lending protocol", "slug": "aave-protocol-guide"},
        {"title": "Curve Finance: Stablecoin Swapping Optimized", "topic": "Curve Finance", "slug": "curve-finance-guide"},
        {"title": "MakerDAO and DAI: Stablecoin Mechanisms Explained", "topic": "MakerDAO DAI", "slug": "makerdao-guide"},
        {"title": "Compound Finance: Earning Interest on Crypto", "topic": "Compound Finance", "slug": "compound-finance-guide"},
        {"title": "Yearn Finance: Yield Optimization Strategies", "topic": "Yearn Finance", "slug": "yearn-finance-guide"},
        {"title": "Impermanent Loss in Liquidity Pools: What It Is and How to Avoid It", "topic": "impermanent loss", "slug": "impermanent-loss-guide"},
        {"title": "Flash Loans: The DeFi Innovation Shaking the Market", "topic": "flash loans DeFi", "slug": "flash-loans-guide"},
        {"title": "Governance Tokens: Voting Power in DeFi", "topic": "governance tokens", "slug": "governance-tokens-guide"},
        {"title": "Decentralized Derivatives: Trading Without Intermediaries", "topic": "decentralized derivatives", "slug": "decentralized-derivatives"},
        
        # Investing & Analysis (10)
        {"title": "Fundamental Analysis for Cryptocurrency: Valuation Metrics", "topic": "crypto fundamental analysis", "slug": "crypto-fundamental-analysis"},
        {"title": "Cryptocurrency Market Cap Explained: What It Really Means", "topic": "crypto market cap", "slug": "market-cap-explained"},
        {"title": "On-Chain Analysis: Reading Blockchain Data Like an Expert", "topic": "on-chain analysis", "slug": "on-chain-analysis-guide"},
        {"title": "Whale Watching in Crypto: What Large Holders Are Doing", "topic": "crypto whale watching", "slug": "whale-watching-guide"},
        {"title": "Dollar Cost Averaging in Crypto: Reduce Risk, Build Wealth", "topic": "DCA crypto strategy", "slug": "dca-crypto-strategy"},
        {"title": "Portfolio Allocation for Crypto: Diversification Strategies", "topic": "crypto portfolio allocation", "slug": "crypto-portfolio-allocation"},
        {"title": "Bull Runs and Bear Markets: Identifying Crypto Cycles", "topic": "crypto market cycles", "slug": "crypto-cycles-guide"},
        {"title": "HODL vs Trading: Which Strategy Makes More Money?", "topic": "hodl vs trading", "slug": "hodl-vs-trading"},
        {"title": "Crypto Tax Implications: What You Need to Know", "topic": "crypto taxes", "slug": "crypto-tax-guide"},
        {"title": "Institutional Adoption: Why Bitcoin Matters More Now", "topic": "institutional crypto adoption", "slug": "institutional-adoption-guide"},
        
        # Specific Coins (15)
        {"title": "Bitcoin Halving Explained: Impact on Price and Mining", "topic": "bitcoin halving", "slug": "bitcoin-halving-guide"},
        {"title": "Litecoin vs Bitcoin: The Silver vs Gold of Crypto", "topic": "litecoin bitcoin", "slug": "litecoin-vs-bitcoin"},
        {"title": "Ripple and XRP: Understanding the Controversial Coin", "topic": "ripple XRP", "slug": "ripple-xrp-guide"},
        {"title": "Cardano: The Blockchain Aiming for Academic Rigor", "topic": "Cardano blockchain", "slug": "cardano-guide"},
        {"title": "Dogecoin: From Meme to Mainstream Cryptocurrency", "topic": "Dogecoin", "slug": "dogecoin-guide"},
        {"title": "Monero: Privacy Coin and Its Controversies", "topic": "Monero privacy coin", "slug": "monero-guide"},
        {"title": "Chainlink: Oracle Network for Smart Contracts", "topic": "Chainlink oracle", "slug": "chainlink-guide"},
        {"title": "Polygon: Scaling Ethereum for the Masses", "topic": "Polygon Ethereum scaling", "slug": "polygon-guide"},
        {"title": "Avalanche: Fast and Scalable Blockchain", "topic": "Avalanche blockchain", "slug": "avalanche-guide"},
        {"title": "Arbitrum: Layer 2 Solution Explained", "topic": "Arbitrum layer 2", "slug": "arbitrum-guide"},
        {"title": "Optimism: Building the Ethereum Layer 2", "topic": "Optimism layer 2", "slug": "optimism-guide"},
        {"title": "Base Blockchain: Coinbase's Layer 2 Solution", "topic": "Base blockchain", "slug": "base-blockchain-guide"},
        {"title": "ZK Rollups: The Future of Ethereum Scaling", "topic": "ZK rollups", "slug": "zk-rollups-guide"},
        {"title": "Bitcoin Lightning Network: Instant Payments", "topic": "lightning network", "slug": "lightning-network-guide"},
        {"title": "Stablecoins Compared: USDC, USDT, DAI, and More", "topic": "stablecoins comparison", "slug": "stablecoins-compared"},
        
        # Emerging Topics (15)
        {"title": "AI and Cryptocurrency: The Convergence", "topic": "AI cryptocurrency", "slug": "ai-crypto-convergence"},
        {"title": "Decentralized Identity: Owning Your Data", "topic": "decentralized identity", "slug": "decentralized-identity-guide"},
        {"title": "Carbon Neutral Crypto: Green Blockchain Solutions", "topic": "green crypto", "slug": "green-crypto-guide"},
        {"title": "Metaverse Cryptocurrencies: Virtual Worlds, Real Money", "topic": "metaverse crypto", "slug": "metaverse-crypto-guide"},
        {"title": "GameFi: Earning While Playing", "topic": "GameFi play to earn", "slug": "gamefi-guide"},
        {"title": "Social Tokens: Monetizing Your Influence", "topic": "social tokens", "slug": "social-tokens-guide"},
        {"title": "CBDCs: Central Bank Digital Currencies Explained", "topic": "CBDC digital currency", "slug": "cbdc-guide"},
        {"title": "Bitcoin as Store of Value: Digital Gold Thesis", "topic": "bitcoin store of value", "slug": "bitcoin-store-value"},
        {"title": "Cryptocurrency Regulation: Global Overview", "topic": "crypto regulation", "slug": "crypto-regulation-guide"},
        {"title": "Quantum Computing and Crypto: Future Threats", "topic": "quantum computing crypto", "slug": "quantum-crypto-guide"},
        {"title": "Cryptocurrency Mining Profitability in 2024", "topic": "crypto mining profitable", "slug": "crypto-mining-2024"},
        {"title": "Cloud Mining: Legitimate or Scam?", "topic": "cloud mining", "slug": "cloud-mining-guide"},
        {"title": "Cryptocurrency Loans and Borrowing", "topic": "crypto loans", "slug": "crypto-loans-guide"},
        {"title": "Insurance for Cryptocurrency Holdings", "topic": "crypto insurance", "slug": "crypto-insurance-guide"},
        {"title": "Cryptocurrency Gift Taxes: Legal Implications", "topic": "crypto gift taxes", "slug": "crypto-gift-taxes"},
    ]
    return topics

def generate_article_content(title, topic):
    """Generate SEO-optimized article content"""
    
    content = f"""
    <h2>Introduction to {topic}</h2>
    <p>This comprehensive guide covers everything you need to know about {topic}. Whether you're a beginner or experienced investor, understanding these concepts is crucial for success in the cryptocurrency space.</p>
    
    <h2>Key Benefits</h2>
    <ul>
        <li><strong>Accessibility:</strong> Start with small investments and grow over time</li>
        <li><strong>Security:</strong> Learn industry-standard security practices</li>
        <li><strong>Returns:</strong> Understand potential returns and risks</li>
        <li><strong>Flexibility:</strong> Manage your portfolio anytime, anywhere</li>
        <li><strong>Community:</strong> Join thousands of active investors</li>
    </ul>
    
    <h2>Getting Started</h2>
    <p>The cryptocurrency market is accessible to everyone. Start with education, use secure wallets, and never invest money you can't afford to lose. This is the foundation of successful crypto investing.</p>
    
    <h2>Best Practices</h2>
    <ul>
        <li>Use hardware wallets for large holdings</li>
        <li>Enable two-factor authentication (2FA)</li>
        <li>Research before investing</li>
        <li>Diversify your portfolio</li>
        <li>Keep emergency savings separate</li>
    </ul>
    
    <h2>Common Mistakes to Avoid</h2>
    <p>New investors often make mistakes like investing without research, using weak passwords, sharing seed phrases, and panic selling. Learn from others' mistakes to protect your investments.</p>
    
    <h2>Future Opportunities</h2>
    <p>{topic.title()} represents an important part of the modern financial landscape. Understanding its nuances will help you make informed decisions in your financial journey.</p>
    """
    
    return content

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
    log_message(f"✓ Topic pool contains {len(topics)} unique topics")
    generated_count = 0

    # Filter out topics that were already generated, THEN sample.
    # This guarantees fresh articles every run as long as any unused
    # topic remains, instead of randomly sampling and discarding hits.
    used_slugs = {art["slug"] for art in previously_generated}
    available_topics = [t for t in topics if t["slug"] not in used_slugs]

    if not available_topics:
        log_message("⚠ All topics have been used! Consider expanding the topic pool further.")
        available_topics = topics  # fall back to allowing repeats rather than failing

    selected_topics = random.sample(
        available_topics, min(ARTICLE_COUNT, len(available_topics))
    )

    for topic_data in selected_topics:
        title = topic_data["title"]
        topic = topic_data["topic"]
        slug = topic_data["slug"]

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
