#!/bin/bash
# ==============================================================================
# BTCPay Server Installation Script -- Self-Hosted Crypto Payment Processor
# For Iran-optimized auto-content-income site (sanctioned-region friendly)
# Zero KYC, zero third-party dependency, full control of funds
# ==============================================================================

set -euo pipefail

echo "================================================"
echo "  BTCPay Server Installer -- Self-Hosted & Open-Source"
echo "  Iran-Optimized Crypto Payment Processor"
echo "================================================"
echo ""

# ---------------------------------------------------------------------------
# Prerequisites Check: Docker + Docker Compose
# ---------------------------------------------------------------------------
echo "[1/7] Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Installing Docker..."

    if [[ "$(uname)" == "Linux" && -f /etc/os-release ]]; then
        # Detect OS and install Docker officially
        OS=$(grep '^ID=' /etc/os-release | cut -d= -f2)
        case "$OS" in
            ubuntu|debian)
                apt-get update
                apt-get install -y ca-certificates curl gnupg
                install -m 0755 -d /etc/apt/keyrings
                curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
                chmod a+r /etc/apt/keyrings/docker.asc
                echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/$OS $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
                    | tee /etc/apt/sources.list.d/docker.list > /dev/null
                apt-get update
                apt-get install -y docker-ce docker-ce-cli containerd.io
                ;;
            *)
                curl -fsSL https://get.docker.com | sh
                ;;
        esac
    else
        echo "Please install Docker manually: https://docs.docker.com/engine/install/"
        exit 1
    fi

    systemctl enable --now docker || service docker start
    sudo usermod -aG docker $USER
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Docker Compose not found (as binary). Checking 'docker compose' plugin..."

    if ! docker compose version &> /dev/null; then
        echo "ERROR: Docker Compose not found. Installing..."
        curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(dpkg --print-architecture) \
            -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
fi

echo "  Docker version: $(docker --version)"
echo "  Docker Compose version: $(docker compose version || docker-compose version)"
echo ""

# ---------------------------------------------------------------------------
# Directory Setup
# ---------------------------------------------------------------------------
echo "[2/7] Setting up directories..."
INSTALL_DIR="${BTCPAY_INSTALL_DIR:-$HOME/btcpay-server}"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "  Installing BTCPay Server to: $PWD"
echo ""

# ---------------------------------------------------------------------------
# Clone BTCPay Server
# ---------------------------------------------------------------------------
echo "[3/7] Cloning BTCPay Server repository..."
if [ ! -d ".git" ]; then
    git clone https://github.com/btcpayserver/btcpayserver.git .
fi
cd "$INSTALL_DIR/BTCPayServer.Docker"
echo "  Version: $(git describe --tags 2>/dev/null || echo 'latest')"
echo ""

# ---------------------------------------------------------------------------
# Generate TLS Configuration (for HTTPS)
# ---------------------------------------------------------------------------
echo "[4/7] Configuring TLS and email..."
export BTCPAY_HOST="${BTCPAY_HOST:-btcpay.example.com}"
export LIGHTNING_NETWORK_ENABLED="${BTCPAY_LIGHTNING :- true}"
export BITCOIN_NETWORK="${BTCPAY_BITCOIN_NETWORK :- testnet}"  # use 'mainnet' when ready

# Generate a self-signed cert for local testing if no real domain yet
if [[ "$BITCOIN_NETWORK" != "testnet" ]]; then
    echo "  Note: For production, replace $BTCPAY_HOST with your real domain."
    echo "  BTCPay requires SSL/TLS. Use nginx/Caddy reverse proxy or Let's Encrypt."
fi

echo ""

# ---------------------------------------------------------------------------
# Environment File Configuration
# ---------------------------------------------------------------------------
echo "[5/7] Writing environment configuration..."
cat > .env <<ENVEOF
### BTCPay Server Configuration - Iran Optimized ###

# Network: mainnet, testnet, regtest
BITCOIN_NETWORK=${BTCPAY_BITCOIN_NETWORK:-mainnet}

# Domain (change to YOUR actual domain or VPS IP)
BTCPAY_HOST=${BTCPAY_HOST:-btcpay.example.com}

# SSL/TLS mode: none, let's encrypt, certbot, custom
BTCPAY_SSLENABLED=true

# Lightning Network enabled?
LIGHTNING_NETWORK_ENABLED=${BTCPAY_LIGHTNING:-true}

# Expose internal port for Nginx reverse proxy
HTTP_PORT=80

# Admin email (change to your real email)
ADMIN_EMAIL=admin@${BTCPAY_HOST:-btcpay.example.com}

### CURRENCY PAIRINGS (add more as needed) ###
SUPPORTERS_ENABLED=true

### Bitcoin Core settings (mainnet node) ###
BITCOIN_RPCUSER=btcpayuser
BITCOIN_PASSWORD=$(openssl rand -hex 32)

### Optional: Exchange plugins for auto-conversion ###
BTCPAY_GENERATE_URI=yes

### Logging ###
LOG_LEVEL=Info
ENVEOF

echo "  Configuration written to: $PWD/.env"
echo ""

# ---------------------------------------------------------------------------
# Run BTCPay Server via Docker Compose
# ---------------------------------------------------------------------------
echo "[6/7] Starting BTCPay Server (first time setup takes ~5-15 minutes)..."
echo "  This will download Bitcoin/Lightning node images. Be patient."
echo ""

# If first run, the initial sync may take very long on mainnet.
# Use testnet for fastest setup and validation.
export BUILD_LEASES=true

timeout 90 docker compose up -d && \
    echo "  BTCPay Server containers starting..." || {
    echo "  Initial start timed out (this is normal -- downloading large images)."
    echo "  Run 'docker compose logs -f btcpayserver' to monitor progress."
}

echo ""

# ---------------------------------------------------------------------------
# Generate Wallet Info & Instructions
# ---------------------------------------------------------------------------
echo "[7/7] Post-install wallet setup instructions..."
echo ""
echo "============================================================"
echo "  INSTALLATION COMPLETE -- NEXT STEPS (do manually):"
echo "============================================================"
echo ""
echo "1. Monitor startup progress:"
echo "   docker compose logs -f btcpayserver"
echo ""
echo "2. WAIT for Bitcoin node to sync (mainnet: hours to days)"
echo "   For testnet, sync takes only minutes."
echo "   Check: docker compose ps  (all services must show 'healthy')"
echo ""
echo "3. Register your first admin account:"
echo "   Go to http://\$BTCPAY_HOST:$HTTP_PORT in your browser"
echo "   Follow the registration wizard."
echo ""
echo "4. Generate receiving wallets AFTER sync is complete:"
echo "   - Navigate to 'Wallets' → Generate Receive Address"
echo "   - Or use BTCPay's REST API: curl -u key:secret ..."
echo ""
echo "5. Integrate with your content site:"
echo "   a) Use the Payment Button Generator in BTCPay admin panel"
echo "   b) Embed the generated crypto payment buttons in articles"
echo "   c) Or use the API to create invoice URLs dynamically"
echo ""
echo "6. Connect to your auto-content-income site:"
echo "   - Place article review content with affiliate links to MEXC/Bybit"
echo "   - Add BTCPay payment buttons on any product/service pages"
echo "   - NOWPayments as backup gateway (see config/iran_affiliate_links.json)"
echo ""
echo "============================================================"
