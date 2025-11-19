# Fleet Logistics API - Quick Reference

## Base URL
- Local: `http://localhost:8000`
- Railway: `https://your-app.railway.app`

## Common Query Parameters

Most list endpoints support:
- `skip` - Number of records to skip (pagination)
- `limit` - Maximum number of records to return
- Entity-specific filters (see below)

## Status Values

### Vehicle Status
- `active` - Currently operational
- `maintenance` - Under maintenance
- `retired` - No longer in service

### Route Status
- `scheduled` - Not yet started
- `in_progress` - Currently active
- `completed` - Finished
- `cancelled` - Cancelled

### Delivery Status
- `pending` - Not yet picked up
- `in_transit` - On the way
- `delivered` - Successfully delivered
- `failed` - Delivery failed

### Delivery Priority
- `standard` - Normal priority
- `express` - Higher priority
- `urgent` - Highest priority

### Driver Status
- `active` - Currently working
- `inactive` - Not currently working
- `on_leave` - On leave

### Incident Severity
- `minor` - Small issue
- `moderate` - Medium severity
- `major` - Serious issue
- `critical` - Critical incident

## Example API Calls for Postman

### 1. Get All Deliveries (with filters)
```
GET /deliveries/?status=in_transit&limit=50
GET /deliveries/?priority=urgent
GET /deliveries/?route_id=1
```

### 2. Track a Specific Delivery
```
GET /deliveries/tracking/TRK123456789
```

### 3. Get Vehicles by Status
```
GET /vehicles/?status=active
GET /vehicles/?vehicle_type=semi_truck
GET /vehicles/?organization_id=1
```

### 4. Get Routes for a Specific Driver
```
GET /routes/?driver_id=5&status=completed
```

### 5. Get Maintenance Records for a Vehicle
```
GET /maintenance/?vehicle_id=10&maintenance_type=repair
```

### 6. Get Fuel Logs for Analysis
```
GET /fuel/?vehicle_id=15
GET /fuel/?fuel_type=diesel
```

### 7. Get Latest GPS Location
```
GET /gps/vehicle/20/latest
GET /gps/?vehicle_id=20&limit=100
```

### 8. Get Incidents by Driver
```
GET /incidents/?driver_id=8
GET /incidents/?severity=major&resolved=false
```

### 9. Get Locations by Type
```
GET /locations/?type=warehouse
GET /locations/?city=Los Angeles&state=CA
```

### 10. Create a New Delivery (POST)
```json
POST /deliveries/
{
  "route_id": 1,
  "location_id": 10,
  "tracking_number": "TRK999999999",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "555-0123",
  "package_count": 5,
  "weight_kg": 25.5,
  "status": "pending",
  "priority": "standard",
  "scheduled_delivery": "2024-12-25T10:00:00",
  "signature_required": true
}
```

## Complex Query Examples

### Fleet Utilization Report
1. Get all active vehicles: `GET /vehicles/?status=active`
2. For each vehicle, get recent routes: `GET /routes/?vehicle_id={id}&status=completed`
3. Calculate metrics from the data

### Driver Performance Analysis
1. Get driver details: `GET /drivers/{driver_id}`
2. Get all completed routes: `GET /routes/?driver_id={id}&status=completed`
3. Check for incidents: `GET /incidents/?driver_id={id}`
4. Calculate on-time delivery rate

### Maintenance Cost Analysis
1. Get all vehicles: `GET /vehicles/`
2. For each vehicle, get maintenance records: `GET /maintenance/?vehicle_id={id}`
3. Aggregate costs and downtime

### Delivery Tracking Workflow
1. Search by tracking number: `GET /deliveries/tracking/{tracking_number}`
2. Get route details: `GET /routes/{route_id}`
3. Get vehicle location: `GET /gps/vehicle/{vehicle_id}/latest`
4. Estimate arrival time based on distance and speed

## Testing Scenarios for Agents

### Scenario 1: Find Vehicles Needing Maintenance
```
1. GET /vehicles/?status=maintenance
2. GET /maintenance/?vehicle_id={id}
3. Analyze downtime and costs
```

### Scenario 2: Track High-Priority Deliveries
```
1. GET /deliveries/?priority=urgent&status=in_transit
2. For each delivery, GET /routes/{route_id}
3. GET /gps/vehicle/{vehicle_id}/latest
4. Calculate ETA
```

### Scenario 3: Driver Incident Report
```
1. GET /incidents/?resolved=false
2. GET /drivers/{driver_id} for each incident
3. Generate report of unresolved incidents
```

### Scenario 4: Fuel Efficiency Analysis
```
1. GET /vehicles/
2. For each vehicle, GET /fuel/?vehicle_id={id}
3. Calculate average fuel consumption
4. Identify least efficient vehicles
```

### Scenario 5: Route Optimization Opportunities
```
1. GET /routes/?status=completed
2. Analyze distance vs actual time
3. GET /incidents/?incident_type=delay
4. Identify routes with frequent delays
```

## Response Format

All responses follow this pattern:

**Single Resource:**
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2",
  "created_at": "2024-01-01T00:00:00"
}
```

**List of Resources:**
```json
[
  {
    "id": 1,
    "field1": "value1"
  },
  {
    "id": 2,
    "field1": "value2"
  }
]
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

Currently no rate limiting is implemented. This is a development/testing API.

## Authentication

Currently no authentication is required. This is a development/testing API.

## Tips for Postman Collections

1. **Use Environment Variables**
   - Create a Postman environment
   - Set `base_url` variable to your API URL
   - Use `{{base_url}}` in requests

2. **Create Test Scripts**
   - Verify status codes
   - Check response structure
   - Extract IDs for chained requests

3. **Use Collection Variables**
   - Store IDs from responses
   - Use in subsequent requests
   - Example: `pm.collectionVariables.set("vehicle_id", responseData.id)`

4. **Organize by Entity**
   - Create folders for each entity type
   - Add common queries to each folder
   - Use descriptive names

5. **Pre-request Scripts**
   - Generate random data for POST requests
   - Set up authentication tokens (when added)
   - Validate data before sending
