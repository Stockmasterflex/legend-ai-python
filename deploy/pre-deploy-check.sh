#!/bin/bash
# Pre-deployment validation script
# Checks system requirements and dependencies

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Running pre-deployment checks...${NC}"

# Check Python version
echo -n "Checking Python version... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 11 ]; then
        echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
    else
        echo -e "${RED}✗ Python 3.11+ required (found $PYTHON_VERSION)${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python not found${NC}"
    exit 1
fi

# Check Git status
echo -n "Checking Git status... "
if git diff-index --quiet HEAD --; then
    echo -e "${GREEN}✓ Working directory clean${NC}"
else
    echo -e "${YELLOW}⚠ Uncommitted changes detected${NC}"
fi

# Check if on correct branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Check disk space
echo -n "Checking disk space... "
AVAILABLE=$(df -h . | awk 'NR==2 {print $4}')
echo -e "${GREEN}✓ Available: $AVAILABLE${NC}"

# Check requirements.txt exists
echo -n "Checking requirements.txt... "
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
    exit 1
fi

# Check critical files
CRITICAL_FILES=(
    "app/main.py"
    "app/config.py"
    "app/models.py"
    "Dockerfile"
    "railway.toml"
)

echo "Checking critical files..."
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file (missing)"
        exit 1
    fi
done

# Run Python syntax check
echo -n "Checking Python syntax... "
if python3 -m py_compile app/main.py 2>/dev/null; then
    echo -e "${GREEN}✓ Valid${NC}"
else
    echo -e "${RED}✗ Syntax errors detected${NC}"
    exit 1
fi

# Check if tests pass (optional)
if [ -f "pytest.ini" ] && command -v pytest &> /dev/null; then
    echo "Running test suite..."
    if pytest tests/ -v --tb=short -x; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${RED}✗ Tests failed${NC}"
        echo -e "${YELLOW}Continue anyway? (y/N)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

echo -e "${GREEN}✓ All pre-deployment checks passed!${NC}"
exit 0
