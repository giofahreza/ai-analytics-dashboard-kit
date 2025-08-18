#!/bin/bash

# TINSIG AI Dashboard - Service Runner (Shell Script Version)
# Starts all required services for the dashboard

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
AGENT_DIR="$SCRIPT_DIR/agent"
VENV_PYTHON="$AGENT_DIR/venv/bin/python"

# Function to print status
print_status() {
    local service=$1
    local message=$2
    local color=${3:-$NC}
    echo -e "${color}[${service}]${NC} ${message}"
}

# Function to check dependencies
check_dependencies() {
    echo -e "\n${BOLD}🔍 Checking dependencies...${NC}"
    
    # Check PHP
    if ! command -v php &> /dev/null; then
        print_status "ERROR" "PHP not found! Please install PHP." $RED
        exit 1
    fi
    print_status "PHP" "Available ✓" $GREEN
    
    # Check Python virtual environment
    if [ ! -f "$VENV_PYTHON" ]; then
        print_status "ERROR" "Python virtual environment not found at: $VENV_PYTHON" $RED
        exit 1
    fi
    print_status "PYTHON" "Virtual environment found ✓" $GREEN
    
    # Check directories
    for dir in "source1" "source2" "source3" "agent/backend" "agent/frontend"; do
        if [ ! -d "$SCRIPT_DIR/$dir" ]; then
            print_status "ERROR" "Directory not found: $SCRIPT_DIR/$dir" $RED
            exit 1
        fi
    done
    
    print_status "DEPS" "All dependencies available ✓" $GREEN
}

# Function to cleanup processes on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping all services...${NC}"
    
    # Kill all background jobs
    jobs -p | xargs -r kill
    
    # Kill specific processes by port
    for port in 8001 8002 8003 8000 8502; do
        pid=$(lsof -t -i:$port 2>/dev/null)
        if [ ! -z "$pid" ]; then
            kill $pid 2>/dev/null
            print_status "PORT $port" "Stopped" $YELLOW
        fi
    done
    
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Function to start PHP server
start_php_server() {
    local source_num=$1
    local port=$2
    local source_dir="$SCRIPT_DIR/source$source_num"
    
    print_status "PHP API $source_num" "Starting on port $port..." $YELLOW
    
    cd "$source_dir"
    php -S localhost:$port > /dev/null 2>&1 &
    local pid=$!
    
    # Wait a bit and check if it started
    sleep 1
    if kill -0 $pid 2>/dev/null; then
        print_status "PHP API $source_num" "Running on http://localhost:$port ✓" $GREEN
        return 0
    else
        print_status "PHP API $source_num" "Failed to start ✗" $RED
        return 1
    fi
}

# Function to start backend
start_backend() {
    print_status "BACKEND" "Starting FastAPI server..." $YELLOW
    
    cd "$AGENT_DIR/backend"
    PYTHONPATH=.. "$VENV_PYTHON" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload > /dev/null 2>&1 &
    local pid=$!
    
    # Wait for backend to start
    sleep 3
    if kill -0 $pid 2>/dev/null; then
        # Check if the service is responding
        if curl -s http://127.0.0.1:8000/health > /dev/null; then
            print_status "BACKEND" "Running on http://127.0.0.1:8000 ✓" $GREEN
            return 0
        fi
    fi
    
    print_status "BACKEND" "Failed to start ✗" $RED
    return 1
}

# Function to start frontend
start_frontend() {
    print_status "FRONTEND" "Starting Streamlit app..." $YELLOW
    
    cd "$AGENT_DIR"
    "$VENV_PYTHON" -m streamlit run frontend/app.py --server.port 8502 > /dev/null 2>&1 &
    local pid=$!
    
    # Wait for frontend to start
    sleep 3
    if kill -0 $pid 2>/dev/null; then
        print_status "FRONTEND" "Running on http://localhost:8502 ✓" $GREEN
        return 0
    else
        print_status "FRONTEND" "Failed to start ✗" $RED
        return 1
    fi
}

# Function to show status
show_status() {
    echo -e "\n${BOLD}${GREEN}✅ All Services Started Successfully!${NC}"
    echo -e "\n${BOLD}📋 Service URLs:${NC}"
    echo -e "  🌐 ${CYAN}Web Dashboard:${NC}      http://localhost:8502"
    echo -e "  🔧 ${BLUE}API Documentation:${NC}  http://127.0.0.1:8000/docs"
    echo -e "  ❤️  ${GREEN}API Health Check:${NC}   http://127.0.0.1:8000/health"
    echo -e "\n${BOLD}📊 Data Sources:${NC}"
    echo -e "  🚫 ${RED}Illegal Mining API:${NC}  http://localhost:8001"
    echo -e "  ⛏️  ${GREEN}Production API:${NC}     http://localhost:8002"
    echo -e "  📜 ${BLUE}IUP API:${NC}            http://localhost:8003"
    
    echo -e "\n${BOLD}🎯 Quick Start:${NC}"
    echo -e "  1. Open ${CYAN}http://localhost:8502${NC} in your browser"
    echo -e "  2. Try: '${YELLOW}Add chart view for illegal mining in Jakarta${NC}'"
    echo -e "  3. Try: '${YELLOW}Add map view for production data${NC}'"
    
    echo -e "\n${BOLD}🛑 To stop all services:${NC} Press ${RED}Ctrl+C${NC}"
    echo -e "${MAGENTA}$(printf '=%.0s' {1..60})${NC}"
}

# Main execution
main() {
    echo -e "\n${BOLD}${BLUE}🚀 TINSIG AI Dashboard - Service Manager${NC}"
    echo -e "${CYAN}Starting all services...${NC}\n"
    
    # Check dependencies
    check_dependencies
    
    # Start PHP API servers
    echo -e "\n${BOLD}📡 Starting API Services...${NC}"
    start_php_server 1 8001 || exit 1
    start_php_server 2 8002 || exit 1  
    start_php_server 3 8003 || exit 1
    
    # Start backend
    echo -e "\n${BOLD}⚡ Starting Backend Service...${NC}"
    start_backend || exit 1
    
    # Start frontend
    echo -e "\n${BOLD}🌐 Starting Frontend Service...${NC}"
    start_frontend || exit 1
    
    # Show status and wait
    show_status
    
    # Wait indefinitely
    while true; do
        sleep 1
    done
}

# Show help if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo -e "${BOLD}TINSIG AI Dashboard - Service Manager${NC}

This script starts all required services for the TINSIG AI Dashboard:
- 3 PHP API servers for data sources  
- 1 FastAPI backend server
- 1 Streamlit frontend application

${BOLD}Usage:${NC}
  ./run_services.sh          Start all services
  ./run_services.sh --help   Show this help

${BOLD}Requirements:${NC}
- PHP installed and available in PATH
- Python virtual environment at agent/venv/
- All source directories (source1, source2, source3) present
- Backend and frontend code in agent/ directory

${BOLD}Services:${NC}
- Frontend:        http://localhost:8502
- Backend API:     http://127.0.0.1:8000
- Illegal Mining:  http://localhost:8001
- Production:      http://localhost:8002
- IUP Data:        http://localhost:8003
"
    exit 0
fi

# Run main function
main
