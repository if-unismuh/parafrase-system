#!/bin/bash

# Start script for Paraphrase Backend API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the correct directory
if [ ! -f "app/main.py" ]; then
    print_error "Please run this script from the paraphrase_backend directory"
    exit 1
fi

# Default values
ENVIRONMENT=${ENVIRONMENT:-"development"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
RELOAD=${RELOAD:-"true"}
LOG_LEVEL=${LOG_LEVEL:-"info"}

print_status "Starting Paraphrase Backend API..."
print_status "Environment: $ENVIRONMENT"
print_status "Host: $HOST"
print_status "Port: $PORT"
print_status "Reload: $RELOAD"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    if [ -f ".env.example" ]; then
        print_status "Creating .env from .env.example..."
        cp .env.example .env
        print_warning "Please update .env file with your configuration"
    else
        print_error ".env.example not found. Please create .env file manually"
        exit 1
    fi
fi

# Check if dependencies are installed
print_status "Checking dependencies..."
if ! python -c "import fastapi, uvicorn" 2>/dev/null; then
    print_error "Dependencies not installed. Please run:"
    echo "pip install -r requirements/dev.txt"
    exit 1
fi

# Check if synonym file exists
if [ ! -f "../sinonim.json" ]; then
    print_warning "sinonim.json not found in parent directory"
    print_status "The API will still work but with limited synonym database"
fi

# Set Python path to include parent directory (for smart_efficient_paraphraser import)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Start the application
print_status "Starting server..."

if [ "$RELOAD" = "true" ]; then
    print_status "Running in development mode with auto-reload"
    uvicorn app.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --reload \
        --log-level "$LOG_LEVEL" \
        --reload-dir app \
        --reload-exclude "*.pyc" \
        --reload-exclude "__pycache__/*"
else
    print_status "Running in production mode"
    uvicorn app.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --log-level "$LOG_LEVEL" \
        --workers 1
fi