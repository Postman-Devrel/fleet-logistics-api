#!/bin/bash

echo "Fleet Logistics API - Setup Script"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL command-line tools not found."
    echo "Make sure PostgreSQL is installed and running."
    echo ""
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env with your database credentials."
else
    echo ".env file already exists."
fi

echo ""
echo "===================================="
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your PostgreSQL database URL"
echo "2. Create the database: createdb fleet_logistics"
echo "3. Seed the database: python scripts/seed_data.py"
echo "4. Run the server: uvicorn app.main:app --reload"
echo ""
echo "The API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "===================================="
