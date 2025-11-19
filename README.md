# Fleet Logistics API

A comprehensive fleet management and logistics tracking system built with FastAPI and PostgreSQL. This backend provides realistic data for testing and development purposes, simulating a full-featured logistics company operation.

## Features

### Core Entities
- **Organizations** - Multi-tenant support for logistics companies
- **Vehicles** - Fleet management with 50 vehicles including various types (cargo vans, trucks, semi-trucks)
- **Drivers** - Driver management with license info, ratings, and status tracking
- **Locations** - Warehouses, depots, distribution centers, and customer locations
- **Routes** - Trip planning with origin/destination, schedules, and status tracking
- **Deliveries** - 1000+ package deliveries with tracking numbers and status updates
- **Maintenance Records** - Service history, costs, and downtime tracking
- **Fuel Logs** - Fuel consumption and cost tracking
- **Incidents** - Accident, delay, and violation reporting
- **GPS Tracking** - Real-time location data for vehicles

### Data Characteristics
- 6 months of historical data
- 50 vehicles across multiple types
- 1000 deliveries with realistic statuses
- Multiple organizations for multi-tenant testing
- GPS tracking data for active vehicles
- Maintenance and fuel records for all vehicles
- Realistic geographic data across the United States

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Primary database
- **Pydantic** - Data validation using Python type hints
- **Faker** - Realistic fake data generation

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd fleet-logistics-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database**
```bash
# Create a local PostgreSQL database
createdb fleet_logistics

# Set the DATABASE_URL environment variable
export DATABASE_URL="postgresql://localhost/fleet_logistics"
```

4. **Run the application**
```bash
uvicorn app.main:app --reload
```

5. **Seed the database with fake data**
```bash
python scripts/seed_data.py
```

6. **Access the API documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Railway Deployment

### Prerequisites
- A GitHub account
- A Railway account (https://railway.app)

### Deployment Steps

1. **Push your code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy to Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the configuration

3. **Add PostgreSQL Database**
   - In your Railway project, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Seed the database**
   - Once deployed, run the seeding script via Railway's terminal or locally:
   ```bash
   # Set Railway's DATABASE_URL locally
   export DATABASE_URL="<your-railway-postgres-url>"
   python scripts/seed_data.py
   ```

5. **Access your API**
   - Railway will provide a public URL (e.g., `https://your-app.railway.app`)
   - Visit `https://your-app.railway.app/docs` for the API documentation

## API Endpoints

### Organizations
- `GET /organizations/` - List all organizations
- `GET /organizations/{id}` - Get organization by ID
- `POST /organizations/` - Create new organization
- `PUT /organizations/{id}` - Update organization
- `DELETE /organizations/{id}` - Delete organization

### Vehicles
- `GET /vehicles/` - List vehicles (filterable by status, type, organization)
- `GET /vehicles/{id}` - Get vehicle by ID
- `POST /vehicles/` - Create new vehicle
- `PUT /vehicles/{id}` - Update vehicle
- `DELETE /vehicles/{id}` - Delete vehicle

### Drivers
- `GET /drivers/` - List drivers (filterable by status, organization)
- `GET /drivers/{id}` - Get driver by ID
- `POST /drivers/` - Create new driver
- `PUT /drivers/{id}` - Update driver
- `DELETE /drivers/{id}` - Delete driver

### Deliveries
- `GET /deliveries/` - List deliveries (filterable by status, priority, route, tracking number)
- `GET /deliveries/{id}` - Get delivery by ID
- `GET /deliveries/tracking/{tracking_number}` - Track delivery by tracking number
- `POST /deliveries/` - Create new delivery
- `PUT /deliveries/{id}` - Update delivery
- `DELETE /deliveries/{id}` - Delete delivery

### Routes
- `GET /routes/` - List routes (filterable by status, vehicle, driver)
- `GET /routes/{id}` - Get route by ID
- `POST /routes/` - Create new route
- `PUT /routes/{id}` - Update route
- `DELETE /routes/{id}` - Delete route

### Locations
- `GET /locations/` - List locations (filterable by type, city, state, organization)
- `GET /locations/{id}` - Get location by ID
- `POST /locations/` - Create new location
- `PUT /locations/{id}` - Update location
- `DELETE /locations/{id}` - Delete location

### Maintenance
- `GET /maintenance/` - List maintenance records (filterable by vehicle, type)
- `GET /maintenance/{id}` - Get maintenance record by ID
- `POST /maintenance/` - Create new maintenance record
- `PUT /maintenance/{id}` - Update maintenance record
- `DELETE /maintenance/{id}` - Delete maintenance record

### Fuel Logs
- `GET /fuel/` - List fuel logs (filterable by vehicle, fuel type)
- `GET /fuel/{id}` - Get fuel log by ID
- `POST /fuel/` - Create new fuel log
- `PUT /fuel/{id}` - Update fuel log
- `DELETE /fuel/{id}` - Delete fuel log

### Incidents
- `GET /incidents/` - List incidents (filterable by driver, type, severity, resolved status)
- `GET /incidents/{id}` - Get incident by ID
- `POST /incidents/` - Create new incident
- `PUT /incidents/{id}` - Update incident
- `DELETE /incidents/{id}` - Delete incident

### GPS Tracking
- `GET /gps/` - List GPS tracking data (filterable by vehicle)
- `GET /gps/vehicle/{vehicle_id}/latest` - Get latest GPS data for a vehicle
- `GET /gps/{id}` - Get GPS tracking record by ID
- `POST /gps/` - Create new GPS tracking record
- `DELETE /gps/{id}` - Delete GPS tracking record

## Testing with Postman

1. **Import the API**
   - Open Postman
   - Use the "Import" feature
   - Enter your API URL with `/openapi.json` (e.g., `https://your-app.railway.app/openapi.json`)
   - Postman will automatically create a collection with all endpoints

2. **Example Test Scenarios**

   **Scenario 1: Track a delivery**
   ```
   GET /deliveries/?status=in_transit
   GET /deliveries/tracking/{tracking_number}
   ```

   **Scenario 2: Monitor vehicle maintenance**
   ```
   GET /vehicles/?status=maintenance
   GET /maintenance/?vehicle_id={vehicle_id}
   ```

   **Scenario 3: Fleet performance analysis**
   ```
   GET /vehicles/
   GET /fuel/?vehicle_id={vehicle_id}
   GET /gps/vehicle/{vehicle_id}/latest
   ```

   **Scenario 4: Driver performance**
   ```
   GET /drivers/{driver_id}
   GET /routes/?driver_id={driver_id}&status=completed
   GET /incidents/?driver_id={driver_id}
   ```

## Testing with Coding Agents

This API is designed to be used for testing coding agents with realistic, complex data:

### Use Cases
1. **API Integration Testing** - Test agents' ability to consume and interact with RESTful APIs
2. **Data Analysis** - Test agents' ability to query and analyze logistics data
3. **Report Generation** - Generate fleet performance reports
4. **Automation** - Create automated workflows for delivery tracking, maintenance scheduling, etc.
5. **Multi-step Operations** - Test complex operations spanning multiple entities

### Example Agent Tasks
- "Find all vehicles due for maintenance"
- "Generate a report of deliveries delayed by more than 2 hours"
- "Calculate total fuel costs for each vehicle over the last month"
- "Identify drivers with unresolved incidents"
- "Track all deliveries for a specific route"

## Database Schema

The database includes the following relationships:
- Organizations have many Vehicles, Drivers, and Locations
- Vehicles have many Routes, Maintenance Records, Fuel Logs, and GPS Tracking data
- Drivers have many Routes and Incidents
- Routes connect Locations and have many Deliveries
- Deliveries are associated with Routes and Locations

## Data Generation

The seeding script (`scripts/seed_data.py`) generates:
- 3 organizations
- 50 vehicles (various makes, models, and types)
- 60 drivers
- 100 locations across the US
- 400 routes
- 1000 deliveries
- Multiple maintenance records per vehicle
- 20-40 fuel logs per vehicle
- Incidents for ~30% of drivers
- GPS tracking data for recent vehicle movement

All data spans a 6-month historical period with realistic dates, statuses, and relationships.

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (automatically set by Railway)
- `PORT` - Port to run the application (automatically set by Railway)

## Project Structure

```
fleet-logistics-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database/
│   │   ├── __init__.py
│   │   └── config.py           # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       ├── organizations.py
│       ├── vehicles.py
│       ├── drivers.py
│       ├── locations.py
│       ├── routes.py
│       ├── deliveries.py
│       ├── maintenance.py
│       ├── fuel.py
│       ├── incidents.py
│       └── gps.py
├── scripts/
│   └── seed_data.py            # Database seeding script
├── requirements.txt
├── Procfile                    # Railway/Heroku deployment
├── railway.json                # Railway configuration
├── .gitignore
└── README.md
```

## License

This project is for testing and development purposes.

## Contributing

Feel free to submit issues and enhancement requests!
