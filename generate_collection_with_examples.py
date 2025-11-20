#!/usr/bin/env python3
"""
Generate a Postman collection with saved examples by calling the live API
"""

import requests
import json
from datetime import datetime

LIVE_API_BASE = "https://web-production-ac9db.up.railway.app"

# Define key endpoints to add examples for
endpoints = [
    # Organizations
    {"method": "GET", "path": "/organizations/", "name": "Get All Organizations"},
    {"method": "GET", "path": "/organizations/1", "name": "Get Organization by ID"},

    # Vehicles
    {"method": "GET", "path": "/vehicles/", "name": "Get All Vehicles"},
    {"method": "GET", "path": "/vehicles/?status=active", "name": "Get Active Vehicles"},
    {"method": "GET", "path": "/vehicles/?status=maintenance", "name": "Get Vehicles in Maintenance"},
    {"method": "GET", "path": "/vehicles/1", "name": "Get Vehicle by ID"},

    # Drivers
    {"method": "GET", "path": "/drivers/", "name": "Get All Drivers"},
    {"method": "GET", "path": "/drivers/?status=active", "name": "Get Active Drivers"},
    {"method": "GET", "path": "/drivers/1", "name": "Get Driver by ID"},

    # Locations
    {"method": "GET", "path": "/locations/", "name": "Get All Locations"},
    {"method": "GET", "path": "/locations/?type=warehouse", "name": "Get Warehouses"},
    {"method": "GET", "path": "/locations/1", "name": "Get Location by ID"},

    # Routes
    {"method": "GET", "path": "/routes/", "name": "Get All Routes"},
    {"method": "GET", "path": "/routes/?status=completed", "name": "Get Completed Routes"},
    {"method": "GET", "path": "/routes/1", "name": "Get Route by ID"},

    # Deliveries
    {"method": "GET", "path": "/deliveries/", "name": "Get All Deliveries"},
    {"method": "GET", "path": "/deliveries/?status=delivered", "name": "Get Delivered Packages"},
    {"method": "GET", "path": "/deliveries/?priority=urgent", "name": "Get Urgent Deliveries"},
    {"method": "GET", "path": "/deliveries/1", "name": "Get Delivery by ID"},

    # Maintenance
    {"method": "GET", "path": "/maintenance/", "name": "Get All Maintenance Records"},
    {"method": "GET", "path": "/maintenance/?vehicle_id=1", "name": "Get Maintenance for Vehicle"},

    # Fuel
    {"method": "GET", "path": "/fuel/", "name": "Get All Fuel Logs"},
    {"method": "GET", "path": "/fuel/?vehicle_id=1", "name": "Get Fuel Logs for Vehicle"},

    # Incidents
    {"method": "GET", "path": "/incidents/", "name": "Get All Incidents"},
    {"method": "GET", "path": "/incidents/?resolved=false", "name": "Get Unresolved Incidents"},

    # GPS Tracking
    {"method": "GET", "path": "/gps/", "name": "Get GPS Tracking Data"},
    {"method": "GET", "path": "/gps/vehicle/1/latest", "name": "Get Latest GPS for Vehicle"},

    # Health
    {"method": "GET", "path": "/health", "name": "Health Check"},
]

def make_request_with_example(endpoint):
    """Make a request and create a Postman item with example"""
    url = LIVE_API_BASE + endpoint['path']
    method = endpoint['method']

    print(f"  {method} {endpoint['path']}")

    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        else:
            return None

        # Parse URL parts
        url_parts = endpoint['path'].split('?')
        path_parts = url_parts[0].strip('/').split('/')
        query_params = []

        if len(url_parts) > 1:
            for param in url_parts[1].split('&'):
                key, value = param.split('=')
                query_params.append({"key": key, "value": value})

        # Create request item
        item = {
            "name": endpoint['name'],
            "request": {
                "method": method,
                "header": [],
                "url": {
                    "raw": url,
                    "protocol": "https",
                    "host": ["web-production-ac9db", "up", "railway", "app"],
                    "path": path_parts,
                }
            },
            "response": [
                {
                    "name": "Example Response",
                    "originalRequest": {
                        "method": method,
                        "header": [],
                        "url": {
                            "raw": url,
                            "protocol": "https",
                            "host": ["web-production-ac9db", "up", "railway", "app"],
                            "path": path_parts,
                        }
                    },
                    "status": f"{response.status_code} {response.reason}",
                    "code": response.status_code,
                    "_postman_previewlanguage": "json",
                    "header": [
                        {"key": k, "value": v}
                        for k, v in response.headers.items()
                    ],
                    "cookie": [],
                    "body": response.text
                }
            ]
        }

        if query_params:
            item['request']['url']['query'] = query_params
            item['response'][0]['originalRequest']['url']['query'] = query_params

        return item

    except Exception as e:
        print(f"    Error: {e}")
        return None

# Create collection structure
print("Generating Postman collection with examples...")
print("="*60)

items = []
for endpoint in endpoints:
    item = make_request_with_example(endpoint)
    if item:
        items.append(item)

collection = {
    "info": {
        "name": "Fleet Logistics API (With Examples)",
        "_postman_id": "fleet-logistics-with-examples",
        "description": "Fleet Logistics API with saved response examples from live data",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": items
}

# Save to file
output_file = "fleet-logistics-collection-with-examples.json"
with open(output_file, 'w') as f:
    json.dump(collection, f, indent=2)

print("="*60)
print(f"✓ Collection generated: {output_file}")
print(f"  Total requests with examples: {len(items)}")
print(f"\nTo import into Postman:")
print(f"  1. Open Postman")
print(f"  2. Click 'Import'")
print(f"  3. Select '{output_file}'")
print(f"  4. Click 'Import'")
