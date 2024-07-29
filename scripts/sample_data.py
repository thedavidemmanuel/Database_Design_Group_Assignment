from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# MongoDB connection
client = MongoClient("mongodb://buoy:sudanman@localhost:27017/water_quality_db?authSource=admin")
db = client.water_quality_db

# Sample data
admin_data = [
    {"name": "John Doe", "email": "john@example.com"},
    {"name": "Jane Smith", "email": "jane@example.com"},
]

location_data = [
    {"name": "River A", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Lake B", "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Ocean C", "latitude": 25.7617, "longitude": -80.1918},
]

# Function to generate random water quality data
def generate_water_quality_data(location_id):
    return {
        "location_id": location_id,
        "ph": round(random.uniform(6.5, 8.5), 2),
        "hardness": round(random.uniform(50, 300), 2),
        "solids": round(random.uniform(300, 1000), 2),
        "chloramines": round(random.uniform(0, 10), 2),
        "sulfate": round(random.uniform(0, 500), 2),
        "conductivity": round(random.uniform(200, 800), 2),
        "organic_carbon": round(random.uniform(1, 20), 2),
        "trihalomethanes": round(random.uniform(0, 100), 2),
        "turbidity": round(random.uniform(1, 10), 2),
        "timestamp": datetime.utcnow() - timedelta(days=random.randint(0, 30))
    }

# Add admin users
admin_collection = db.admin
admin_collection.insert_many(admin_data)
print(f"Added {len(admin_data)} admin users")

# Add locations
location_collection = db.location
location_result = location_collection.insert_many(location_data)
print(f"Added {len(location_data)} locations")

# Add water quality entries
water_quality_collection = db.waterquality
water_quality_entries = []

for location_id in location_result.inserted_ids:
    for _ in range(10):  # 10 entries per location
        water_quality_entries.append(generate_water_quality_data(location_id))

water_quality_collection.insert_many(water_quality_entries)
print(f"Added {len(water_quality_entries)} water quality entries")

print("Data insertion complete")