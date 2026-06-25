# Auto Content Income System — Setup Guide (Iran-Optimized Edition)

## What Changed from the Original

The original system relied on Amazon Associates, ShareASale, Google AdSense, and PayPal for monetization. All of these are blocked or refuse service to users in Iran. This edition replaces every single one with crypto-native alternatives:

| Was Blocked in Iran | Now Works (Crypto Alternative) |
|---------------------|--------------------------------|
| Amazon Associates | MEXC Exchange referral (up to 70% commission, payouts to your wallet in USDT) |
| ShareASale / Impact.com | Bybit Affiliate (40% commission, direct crypto payout) |
| Google AdSense | Adsterra ($5 min, pays in BTC/USDT to any wallet — works from Iran) |
| PayPal / Stripe | NOWPayments (200+ coins accepted, no KYC merchant account), BTCPay Server (self-hosted) |

---

## Step 1: Create Your Free GitHub Pages Website (5 min)

1. Go to **github.com/signup** and create a free account
2. Click **"Create a new repository"**
3. Name it exactly: `yourusername.github.io`
4. Make it **PUBLIC**
5. Click "Create repository"
6. Done! Your site is at `https://yourusername.github.io/`

## Step 2: Install Git (if needed)

```bash
# Check if git is installed:
git --version

# If not installed, use winget (Windows):
winget install --id Git.Git -e --source winget

# Verify and configure:
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Step 3: Sign Up for Crypto Affiliate Programs (Takes ~15 minutes total)

### 3a. MEXC Exchange — Your Highest-Earning Referral Program ⭐⭐⭐⭐⭐
**Commission: Up to 70% of each referred user's trading fees — forever.**

1. Go to **https://www.mexc.com/register?inviteCode=mexc**
2. Register with email (no KYC required for basic trading)
3. Navigate to your **Affiliate / Referral page** after signup
4. Copy your unique referral link (e.g., `https://www.mexc.com/register?inviteCode=YOURCODE`)
5. Paste this URL into `config/iran_affiliate_links.json` under the `"mexc_exchange" → "url"` key
6. **Start earning**: 70% of every user's trading fees for life, paid directly to your wallet

### 3b. Bybit Affiliate — Second-Highest Paying Exchange ⭐⭐⭐⭐⭐
**Commission: 40-50%, daily crypto payout.**

1. Go to **https://partners.bybit.com/** and apply for the affiliate program
2. Get your referral link from the dashboard once approved (usually instant)
3. Paste into `config/iran_affiliate_links.json` under `"bybit_affiliate" → "url"`
4. Bybit supports direct crypto payouts to your wallet and accepts users worldwide including sanctioned regions

### 3c. NOWPayments — Accept Crypto Payments on Your Content Site ⭐⭐⭐⭐
**No KYC, 0.5% transaction fee, 200+ coins accepted.**

1. Go to **https://nowpayments.io/signup**
2. Create a merchant account (no KYC required)
3. Use their dashboard to generate payment buttons for any amount
4. Embed these buttons on your content site pages for donations or product sales
5. Funds go DIRECTLY from customer wallets to your wallets — no platform holds

### 3d. CoinGate — Backup Payment Gateway ⭐⭐⭐⭐
1. Go to **https://www.coingate.com/** and create a merchant account
2. Set up payment acceptance alongside NOWPayments as redundant option
3. Supports fiat off-ramp if you ever need traditional currency conversion

### 3e. Adsterra — Display Ads for Your Content Site ⭐⭐⭐⭐
**$5 minimum payout threshold. Works from Iran.**

1. Go to **https://adsterra.com/register/publisher** and sign up as a publisher
2. Add your GitHub Pages domain
3. Copy the ad code snippets and embed into your `content/templates/index.html` alongside articles
4. Get paid in BTC, USDT (TRC20), or Cosmo Payment — $5 minimum is one of the lowest barriers in the industry. Adsterra pays to any wallet worldwide

### 3f. PropellerAds — Backup Ad Network ⭐⭐⭐
**Alternative ad format inventory. Direct crypto payout.**

1. Go to **https://propellerads.com/register** and sign up as a publisher
2. Provides pop-under, push notification, and native banner formats that complement Adsterra's inventory
3. Payout options include BTC, BCH, USDT, ETH without KYC requirements

## Step 4: Set Up BTCPay Server (Self-Hosted Crypto Payments — Free Forever) ⭐⭐⭐⭐⭐

This is the most powerful addition. You run your own Bitcoin lightning node and payment processor — no platform can freeze your funds or shut down the service.

See `setup/install-btcpay.sh` for full automated Docker-based installation, which includes:
- Bitcoin Core + Lightning Network (LND) node setup on your VPS
- Automated TLS configuration via Let's Encrypt or custom certificates
- Wallet address generation and invoice creation API integration
- Full documentation on integrating payment buttons into your content site

**Minimum VPS specs**: 2 CPU cores, 4GB RAM, 50GB SSD. Providers that accept Bitcoin: BuyVM, VPS.net, HostYours.se (among others). Total cost ~$5-10/month.

## Step 5: Connect Your GitHub Pages Repo to This Project

```bash
# Create a deploy directory  
mkdir /tmp/deploy-acg

# Clone your GitHub Pages repo there (replace YOUR_USERNAME with yours):
git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME.github.io.git /tmp/deploy-acg/
```

## Step 6: Let Hermès Automate Everything Going Forward

After you complete Steps 1-3 (takes ~30 minutes total once):

1. **Confirm your referral links are in `config/iran_affiliate_links.json`** — this is critical because generate_articles.py reads URLs from this config at runtime!
2. **Hermès will run daily** via cron jobs to research trending crypto topics + write articles automatically, embedding MEXC/Bybit/NOWPayments links into every article
3. **Traffic grows over months** as Google indexes all your content
4. **Money comes from**: (a) exchange referral commissions — users trading through your MEXC/Bybit links generate fee revenue for you perpetually, (b) BTCPay payment buttons on content pages accepting Bitcoin directly, (c) Adsterra display ad revenue

### What happens automatically (ZERO manual work after setup):

| Frequency | Automated Task by Hermès |
|-----------|--------------------------|
| Daily (6 AM) | Research trending crypto/trading topics + update topic_database.csv |
| Daily (7 AM) | Write 3 unique SEO articles embedded with MEXC/Bybit affiliate links |
| Daily (7:30 AM) | Generate HTML files + deploy to GitHub Pages |
| Weekly | SEO optimization pass on all existing content |
| Weekly | Competitor analysis — what crypto niches rival sites rank for that you don't? |
| Monthly | Article link audit + BTCPay node health check + affiliate dashboard review |

After step 5 is complete the ONLY thing you'll ever do again:
- Check MEXC/Bybit affiliate dashboards monthly to see your referral earnings (paid in USDT to your wallet — $0 fees)
- Maybe replace a few dead crypto payment links (rarely needed because crypto URLs don't expire like traditional referral programs)

---

## Troubleshooting Setup Issues

| Problem | Solution |
|---------|----------|
| GitHub Pages not loading after upload | Wait 15 minutes. DNS propagation can take time globally. |
| MEXC/Bybit reject your country during signup | Most major crypto exchanges have relaxed regional restrictions since 2024. If rejected, try a different referral link or contact support directly via Telegram/Discord communities. |
| NOWPayments requires KYC in some regions | This is false for basic merchant accounts — they allow payment acceptance without identity verification as long as you never convert to fiat on their platform (just let funds flow directly to your wallet). |
| BTCPay Server node sync takes forever | Use testnet initially ($0, instant sync) to verify your setup works. Then switch to mainnet for real transactions. Mainnet Bitcoin syncing can take hours/days depending on network conditions. |

---

*Updated: 2026-06-25 | Iran-Optimized Edition — All monetization via cryptocurrency payment rails*
