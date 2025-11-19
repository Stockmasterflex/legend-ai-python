#!/bin/bash
# Run load tests with different scenarios

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
BASE_URL="${BASE_URL:-http://localhost:8000}"
RESULTS_DIR="tests/load/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create results directory
mkdir -p "$RESULTS_DIR"

echo -e "${BLUE}Legend AI Load Testing Suite${NC}"
echo -e "${BLUE}Target: $BASE_URL${NC}\n"

# Check if Locust is installed
if ! command -v locust &> /dev/null; then
    echo -e "${YELLOW}Locust not found. Installing...${NC}"
    pip install locust
fi

# Function to run a load test scenario
run_scenario() {
    local name="$1"
    local users="$2"
    local spawn_rate="$3"
    local duration="$4"

    echo -e "\n${GREEN}Running Scenario: $name${NC}"
    echo "  Users: $users"
    echo "  Spawn Rate: $spawn_rate/sec"
    echo "  Duration: $duration"
    echo ""

    locust \
        -f tests/load/locustfile.py \
        --host="$BASE_URL" \
        --users="$users" \
        --spawn-rate="$spawn_rate" \
        --run-time="$duration" \
        --headless \
        --html="${RESULTS_DIR}/${name}_${TIMESTAMP}.html" \
        --csv="${RESULTS_DIR}/${name}_${TIMESTAMP}" \
        --only-summary

    echo -e "${GREEN}✓ $name completed${NC}"
}

# Scenario 1: Baseline (light load)
echo -e "${BLUE}Scenario 1: Baseline Performance${NC}"
run_scenario "baseline" 10 2 "2m"

# Scenario 2: Normal Load
echo -e "\n${BLUE}Scenario 2: Normal Load${NC}"
run_scenario "normal_load" 50 5 "3m"

# Scenario 3: Peak Load
echo -e "\n${BLUE}Scenario 3: Peak Load${NC}"
run_scenario "peak_load" 100 10 "2m"

# Scenario 4: Stress Test
echo -e "\n${BLUE}Scenario 4: Stress Test${NC}"
run_scenario "stress_test" 200 20 "2m"

# Scenario 5: Spike Test
echo -e "\n${BLUE}Scenario 5: Spike Test${NC}"
run_scenario "spike_test" 500 50 "1m"

echo -e "\n${GREEN}All load tests completed!${NC}"
echo -e "${BLUE}Results saved to: $RESULTS_DIR${NC}"
echo ""
echo "View HTML reports:"
ls -1 "$RESULTS_DIR"/*.html | tail -5
echo ""
echo "Summary statistics:"
cat tests/load/results/load_test_results.txt | tail -20
