#!/bin/bash

# ──────────────────────────────────────────────────────────────
# AI Resume Analyzer - Setup Script for Linux/MacOS
# ──────────────────────────────────────────────────────────────

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  AI Resume Analyzer - Global Setup Script              ║"
echo "║  Platform: $(uname -s)                               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${BLUE}[1/5] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Create virtual environment
echo -e "${BLUE}[2/5] Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}[3/5] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}[4/5] Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
echo ""

# Create directories
echo -e "${BLUE}[5/5] Creating data directories...${NC}"
mkdir -p data uploads logs
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo -e "${GREEN}║  ✓ Setup Complete!                                 ║${NC}"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo -e "${YELLOW}To run the application:${NC}"
echo ""
echo "  1. Activate virtual environment:"
echo "     ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "  2. Start the application:"
echo "     ${BLUE}streamlit run ai_resume_analyzer_global.py${NC}"
echo ""
echo "  3. Access in browser:"
echo "     ${BLUE}http://localhost:8501${NC}"
echo ""
echo -e "${YELLOW}For network access from other machines:${NC}"
echo "     ${BLUE}streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0${NC}"
echo ""
