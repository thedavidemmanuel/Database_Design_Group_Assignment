from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_restx import Api, Resource, fields
from bson.objectid import ObjectId
from datetime import datetime
import tensorflow as tf
import logging
from marshmallow import Schema, fields as ma_fields, ValidationError
from functools import wraps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://buoy:sudanman@localhost:27017/water_quality_db?authSource=admin"
mongo = PyMongo(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Flask-RESTX
api = Api(app, version='1.0', title='Water Quality API',
    description='A simple API for managing water quality data')

# Define namespaces
ns_admin = api.namespace('admin', description='Admin operations')
ns_location = api.namespace('location', description='Location operations')
ns_water_quality = api.namespace('water_quality', description='Water quality operations')

# Schemas for validation
class AdminSchema(Schema):
    name = ma_fields.Str(required=True)
    email = ma_fields.Email(required=True)

class LocationSchema(Schema):
    name = ma_fields.Str(required=True)
    latitude = ma_fields.Float(required=True)
    longitude = ma_fields.Float(required=True)

class WaterQualitySchema(Schema):
    location_id = ma_fields.Str(required=True)
    ph = ma_fields.Float(required=True)
    hardness = ma_fields.Float(required=True)
    solids = ma_fields.Float(required=True)
    chloramines = ma_fields.Float(required=True)
    sulfate = ma_fields.Float(required=True)
    conductivity = ma_fields.Float(required=True)
    organic_carbon = ma_fields.Float(required=True)
    trihalomethanes = ma_fields.Float(required=True)
    turbidity = ma_fields.Float(required=True)

# Flask-RESTX models
admin_model = api.model('Admin', {
    'name': fields.String(required=True, description='Admin name'),
    'email': fields.String(required=True, description='Admin email')
})

location_model = api.model('Location', {
    'name': fields.String(required=True, description='Location name'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

water_quality_model = api.model('WaterQuality', {
    'location_id': fields.String(required=True, description='Location ID'),
    'ph': fields.Float(required=True, description='pH level'),
    'hardness': fields.Float(required=True, description='Water hardness'),
    'solids': fields.Float(required=True, description='Total dissolved solids'),
    'chloramines': fields.Float(required=True, description='Chloramines level'),
    'sulfate': fields.Float(required=True, description='Sulfate level'),
    'conductivity': fields.Float(required=True, description='Conductivity'),
    'organic_carbon': fields.Float(required=True, description='Organic carbon'),
    'trihalomethanes': fields.Float(required=True, description='Trihalomethanes'),
    'turbidity': fields.Float(required=True, description='Turbidity')
})

# Error handling decorator
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as err:
            return {"error": "Validation error", "messages": err.messages}, 400
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {"error": "Internal server error"}, 500
    return wrapper

# Admin Routes
@ns_admin.route('')
class AdminList(Resource):
    @api.expect(admin_model)
    @api.response(201, 'Admin added successfully')
    @api.response(400, 'Validation Error')
    @handle_errors
    def post(self):
        """Add a new admin"""
        data = AdminSchema().load(api.payload)
        result = mongo.db.admin.insert_one(data)
        return {"message": "Admin added", "id": str(result.inserted_id)}, 201

@ns_admin.route('/<id>')
@api.response(404, 'Admin not found')
class Admin(Resource):
    @api.response(200, 'Success')
    @handle_errors
    def get(self, id):
        """Get an admin by ID"""
        admin = mongo.db.admin.find_one({"_id": ObjectId(id)})
        if admin:
            admin['_id'] = str(admin['_id'])
            return admin, 200
        return {"message": "Admin not found"}, 404

# Location Routes
@ns_location.route('')
class LocationList(Resource):
    @api.expect(location_model)
    @api.response(201, 'Location added successfully')
    @api.response(400, 'Validation Error')
    @handle_errors
    def post(self):
        """Add a new location"""
        data = LocationSchema().load(api.payload)
        result = mongo.db.location.insert_one(data)
        return {"message": "Location added", "id": str(result.inserted_id)}, 201

    @api.response(200, 'Success')
    @handle_errors
    def get(self):
        """Get all locations"""
        locations = list(mongo.db.location.find())
        for location in locations:
            location['_id'] = str(location['_id'])
        return locations, 200

# Water Quality Routes
@ns_water_quality.route('')
class WaterQualityList(Resource):
    @api.expect(water_quality_model)
    @api.response(201, 'Water quality entry added successfully')
    @api.response(400, 'Validation Error')
    @handle_errors
    def post(self):
        """Add a new water quality entry"""
        data = WaterQualitySchema().load(api.payload)
        data['timestamp'] = datetime.utcnow()
        result = mongo.db.waterquality.insert_one(data)
        return {"message": "Water quality entry added", "id": str(result.inserted_id)}, 201

    @api.response(200, 'Success')
    @handle_errors
    def get(self):
        """Get all water quality entries"""
        entries = list(mongo.db.waterquality.find())
        for entry in entries:
            entry['_id'] = str(entry['_id'])
            entry['location_id'] = str(entry['location_id'])
        return entries, 200

@ns_water_quality.route('/<id>')
@api.response(404, 'Entry not found')
class WaterQuality(Resource):
    @api.response(200, 'Success')
    @handle_errors
    def get(self, id):
        """Get a water quality entry by ID"""
        entry = mongo.db.waterquality.find_one({"_id": ObjectId(id)})
        if entry:
            entry['_id'] = str(entry['_id'])
            entry['location_id'] = str(entry['location_id'])
            return entry, 200
        return {"message": "Entry not found"}, 404

    @api.expect(water_quality_model)
    @api.response(200, 'Water quality entry updated successfully')
    @api.response(400, 'Validation Error')
    @api.response(404, 'Entry not found')
    @handle_errors
    def put(self, id):
        """Update a water quality entry"""
        data = WaterQualitySchema().load(api.payload)
        result = mongo.db.waterquality.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count:
            updated_doc = mongo.db.waterquality.find_one({"_id": ObjectId(id)})
            updated_doc['_id'] = str(updated_doc['_id'])
            updated_doc['location_id'] = str(updated_doc['location_id'])
            return {"message": "Water quality entry updated", "entry": updated_doc}, 200
        return {"message": "Entry not found"}, 404

    @api.response(200, 'Water quality entry deleted successfully')
    @api.response(404, 'Entry not found')
    @handle_errors
    def delete(self, id):
        """Delete a water quality entry"""
        result = mongo.db.waterquality.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"message": "Water quality entry deleted"}, 200
        return {"message": "Entry not found"}, 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')