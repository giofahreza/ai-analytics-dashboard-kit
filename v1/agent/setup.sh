#!/bin/bash

# TINSIG AI Dashboard - Quick Setup Script
# This script sets up the development environment quickly

set -e  # Exit on any error

echo "🏗️  TINSIG AI Dashboard - Quick Setup"
echo "======================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
echo "🐍 Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.11" | bc -l) -eq 1 ]]; then
    echo "⚠️  Python 3.11+ is recommended. You have $PYTHON_VERSION"
fi

# Navigate to agent directory - we're already in the agent directory
echo "📍 Working directory: $(pwd)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔨 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration!"
    echo "📝 Important: Add your GEMINI_API_KEY to .env"
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start PostgreSQL: docker-compose up -d postgres"  
echo "3. Setup database: python scripts/setup_db.py"
echo "4. Start source APIs from root directory:"
echo "   cd source1 && php -S localhost:8001 &"
echo "   cd source2 && php -S localhost:8002 &"
echo "   cd source3 && php -S localhost:8003 &"
echo "5. Ingest data: python scripts/ingest_data.py"
echo "6. Start backend: cd backend && uvicorn main:app --reload"
echo "7. Start frontend: cd frontend && streamlit run app.py"
echo ""
echo "Or use Docker: ./scripts/deploy.sh"
echo ""
