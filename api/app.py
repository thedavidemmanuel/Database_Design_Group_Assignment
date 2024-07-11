import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://buoy:sudanman@localhost:27017/water_quality_db?authSource=admin"
mongo = PyMongo(app)
api = Api(app)

class AdminResource(Resource):
    def get(self, admin_id=None):
        if admin_id:
            admin = mongo.db.admin.find_one({"_id": ObjectId(admin_id)})
            if admin:
                admin['_id'] = str(admin['_id'])
                return admin, 200
            return {"message": "Admin not found"}, 404
        
        admins = list(mongo.db.admin.find())
        for admin in admins:
            admin['_id'] = str(admin['_id'])
        return admins, 200

    def post(self):
        data = request.get_json()
        result = mongo.db.admin.insert_one(data)
        return {"message": "Admin created", "id": str(result.inserted_id)}, 201

class LocationResource(Resource):
    def get(self, location_id=None):
        if location_id:
            location = mongo.db.location.find_one({"_id": ObjectId(location_id)})
            if location:
                location['_id'] = str(location['_id'])
                return location, 200
            return {"message": "Location not found"}, 404
        
        locations = list(mongo.db.location.find())
        for location in locations:
            location['_id'] = str(location['_id'])
        return locations, 200

    def post(self):
        data = request.get_json()
        result = mongo.db.location.insert_one(data)
        return {"message": "Location created", "id": str(result.inserted_id)}, 201

class WaterQualityResource(Resource):
    def get(self, wq_id=None):
        if wq_id:
            wq = mongo.db.waterquality.find_one({"_id": ObjectId(wq_id)})
            if wq:
                wq['_id'] = str(wq['_id'])
                return wq, 200
            return {"message": "Water Quality record not found"}, 404
        
        wqs = list(mongo.db.waterquality.find())
        for wq in wqs:
            wq['_id'] = str(wq['_id'])
        return wqs, 200

    def post(self):
        data = request.get_json()
        result = mongo.db.waterquality.insert_one(data)
        return {"message": "Water Quality record created", "id": str(result.inserted_id)}, 201

api.add_resource(AdminResource, '/admin', '/admin/<string:admin_id>')
api.add_resource(LocationResource, '/location', '/location/<string:location_id>')
api.add_resource(WaterQualityResource, '/waterquality', '/waterquality/<string:wq_id>')

@app.route('/test_db')
def test_db():
    try:
        mongo.db.command('serverStatus')
        return 'Connected to MongoDB!', 200
    except Exception as e:
        return f'Failed to connect to MongoDB. Error: {str(e)}', 500

@app.route('/')
def home():
    return 'Water Quality API is running!', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')