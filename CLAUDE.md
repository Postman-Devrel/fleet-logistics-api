# Fleet Logistics API - Project Context

## Overview
A FastAPI-based fleet management and logistics tracking REST API. Deployed on Railway with PostgreSQL.

## Architecture
- **Framework**: FastAPI
- **Database**: PostgreSQL (hosted on Railway)
- **ORM**: SQLAlchemy 2.0
- **Schemas**: Pydantic v2

## Key Files
- `openapi.yaml` - Complete API specification (use this for building integrations/MCP servers)
- `app/main.py` - FastAPI application entry point
- `app/routers/` - All endpoint handlers (10 resource routers)
- `app/models/` - SQLAlchemy models and Pydantic schemas
- `scripts/seed_data.py` - Database seeding script

## Database (Railway)
- **Internal URL**: `DATABASE_URL` in .env (used by deployed app)
- **Public URL**: `DATABASE_PUBLIC_URL` in .env (used for local dev/seeding)

## Current Data
Seeded with realistic fleet data:
- 3 organizations
- 200 vehicles
- 150 drivers
- 100 locations
- 400 routes
- 10,000 deliveries
- 12 months of history
- Plus: maintenance records, fuel logs, incidents, GPS tracking

## Running Locally
```bash
# Create venv and install deps
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the seed script (uses DATABASE_PUBLIC_URL)
DATABASE_URL="$DATABASE_PUBLIC_URL" python scripts/seed_data.py

# Start the server
uvicorn app.main:app --reload
```

## MCP Server Integration
This API is intended as a foundation for MCP demos. The `openapi.yaml` file contains everything needed to build an MCP server that wraps this API.
