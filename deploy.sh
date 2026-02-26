#!/bin/bash

# ──────────────────────────────────────────────────────────────
# AI Resume Analyzer - Docker Deployment Script
# Platform: Linux/macOS
# ──────────────────────────────────────────────────────────────

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  AI Resume Analyzer - Docker Deployment Script         ║"
echo "║  Platform: Linux/macOS                                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Docker installation
echo -e "${BLUE}[1/4] Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
fi
echo -e "${GREEN}✓ Docker is installed${NC}"
echo ""

# Check Docker Compose
echo -e "${BLUE}[2/4] Checking Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose not found. Installing...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}"
echo ""

# Build Docker image
echo -e "${BLUE}[3/4] Building Docker image...${NC}"
docker-compose build
echo -e "${GREEN}✓ Docker image built successfully${NC}"
echo ""

# Start containers
echo -e "${BLUE}[4/4] Starting containers...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Containers started successfully${NC}"
echo ""

# Final info
echo "╔════════════════════════════════════════════════════════╗"
echo -e "${GREEN}║  ✓ Deployment Complete!                           ║${NC}"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}Access your application:${NC}"
echo "  http://localhost:8501"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  View logs:      docker-compose logs -f"
echo "  Stop:           docker-compose down"
echo "  Restart:        docker-compose restart"
echo ""
