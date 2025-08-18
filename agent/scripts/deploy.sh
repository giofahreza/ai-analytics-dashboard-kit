#!/bin/bash

# TINSIG AI Dashboard Deployment Script
# This script deploys the full TINSIG AI Dashboard stack

set -e  # Exit on any error

echo "🏗️  TINSIG AI Dashboard - Deployment Script"
echo "============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Set deployment type (default: development)
DEPLOYMENT_TYPE=${1:-development}

echo "📍 Deployment Type: $DEPLOYMENT_TYPE"

# Check if .env file exists, if not copy from example
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration before proceeding."
    read -p "Press Enter to continue after editing .env file..."
fi

# Build and start services
echo "🔨 Building and starting services..."

if [ "$DEPLOYMENT_TYPE" = "production" ]; then
    echo "🚀 Starting production deployment..."
    docker-compose -f docker-compose.prod.yml up --build -d
else
    echo "🛠️  Starting development deployment..."
    docker-compose up --build -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
fi

# Check Backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API is not responding"
fi

# Check Frontend
if curl -f http://localhost:8501 > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not responding"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📍 Access points:"
echo "   📊 Dashboard: http://localhost:8501"
echo "   🔧 API Docs:  http://localhost:8000/docs"
echo "   💾 Database: postgres://localhost:5432/tinsig_db"
echo ""
echo "📋 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
