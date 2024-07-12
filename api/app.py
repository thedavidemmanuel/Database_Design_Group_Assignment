from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import tensorflow as tf
import logging
from marshmallow import Schema, fields, ValidationError
from functools import wraps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://buoy:sudanman@localhost:27017/water_quality_db?authSource=admin"
mongo = PyMongo(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the ML model
try:
    model = tf.keras.models.load_model('water_quality_model.h5')
    logger.info("ML model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load ML model: {str(e)}")
    model = None

# Schemas for validation
class AdminSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

class LocationSchema(Schema):
    name = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

class WaterQualitySchema(Schema):
    location_id = fields.Str(required=True)
    ph = fields.Float(required=True)
    hardness = fields.Float(required=True)
    solids = fields.Float(required=True)
    chloramines = fields.Float(required=True)
    sulfate = fields.Float(required=True)
    conductivity = fields.Float(required=True)
    organic_carbon = fields.Float(required=True)
    trihalomethanes = fields.Float(required=True)
    turbidity = fields.Float(required=True)

# Error handling decorator
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as err:
            return jsonify({"error": "Validation error", "messages": err.messages}), 400
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    return wrapper

# Admin Routes
@app.route('/admin', methods=['POST'])
@handle_errors
def add_admin():
    data = AdminSchema().load(request.json)
    result = mongo.db.admin.insert_one(data)
    return jsonify({"message": "Admin added", "id": str(result.inserted_id)}), 201

@app.route('/admin/<id>', methods=['GET'])
@handle_errors
def get_admin(id):
    admin = mongo.db.admin.find_one({"_id": ObjectId(id)})
    if admin:
        admin['_id'] = str(admin['_id'])
        return jsonify(admin), 200
    return jsonify({"message": "Admin not found"}), 404

# Location Routes
@app.route('/location', methods=['POST'])
@handle_errors
def add_location():
    data = LocationSchema().load(request.json)
    result = mongo.db.location.insert_one(data)
    return jsonify({"message": "Location added", "id": str(result.inserted_id)}), 201

@app.route('/location', methods=['GET'])
@handle_errors
def get_locations():
    locations = list(mongo.db.location.find())
    for location in locations:
        location['_id'] = str(location['_id'])
    return jsonify(locations), 200

# Water Quality Routes
@app.route('/water_quality', methods=['POST'])
@handle_errors
def add_water_quality():
    data = WaterQualitySchema().load(request.json)
    data['timestamp'] = datetime.utcnow()
    result = mongo.db.waterquality.insert_one(data)
    return jsonify({"message": "Water quality entry added", "id": str(result.inserted_id)}), 201

@app.route('/water_quality', methods=['GET'])
@handle_errors
def get_water_quality():
    entries = list(mongo.db.waterquality.find())
    for entry in entries:
        entry['_id'] = str(entry['_id'])
        entry['location_id'] = str(entry['location_id'])
    return jsonify(entries), 200

@app.route('/water_quality/<id>', methods=['GET'])
@handle_errors
def get_water_quality_entry(id):
    entry = mongo.db.waterquality.find_one({"_id": ObjectId(id)})
    if entry:
        entry['_id'] = str(entry['_id'])
        entry['location_id'] = str(entry['location_id'])
        return jsonify(entry), 200
    return jsonify({"message": "Entry not found"}), 404

@app.route('/water_quality/<id>', methods=['PUT'])
@handle_errors
def update_water_quality(id):
    data = WaterQualitySchema().load(request.json)
    result = mongo.db.waterquality.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count:
        updated_doc = mongo.db.waterquality.find_one({"_id": ObjectId(id)})
        updated_doc['_id'] = str(updated_doc['_id'])
        updated_doc['location_id'] = str(updated_doc['location_id'])
        return jsonify({"message": "Water quality entry updated", "entry": updated_doc}), 200
    return jsonify({"message": "Entry not found"}), 404

@app.route('/water_quality/<id>', methods=['DELETE'])
@handle_errors
def delete_water_quality(id):
    result = mongo.db.waterquality.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Water quality entry deleted"}), 200
    return jsonify({"message": "Entry not found"}), 404

# Prediction Route
@app.route('/predict', methods=['GET'])
@handle_errors
def predict():
    if model is None:
        return jsonify({"error": "ML model not available"}), 500

    latest_entry = mongo.db.waterquality.find_one(sort=[('_id', -1)])
    
    if not latest_entry:
        return jsonify({"message": "No water quality data available"}), 404
    
    input_data = [
        latest_entry['ph'], latest_entry['hardness'], latest_entry['solids'],
        latest_entry['chloramines'], latest_entry['sulfate'], latest_entry['conductivity'],
        latest_entry['organic_carbon'], latest_entry['trihalomethanes'], latest_entry['turbidity']
    ]
    
    prediction = model.predict([input_data])[0]
    
    mongo.db.waterquality.update_one(
        {"_id": latest_entry['_id']},
        {"$set": {"potability": bool(prediction[0] > 0.5)}}
    )
    
    return jsonify({
        "message": "Prediction made",
        "water_quality_id": str(latest_entry['_id']),
        "prediction": bool(prediction[0] > 0.5),
        "confidence": float(prediction[0])
    }), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')