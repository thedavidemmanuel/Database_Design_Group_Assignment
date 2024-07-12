import unittest
from app import app, mongo
from bson import ObjectId

class TestWaterQualityApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        # Clean up the database before each test
        mongo.db.admin.delete_many({})
        mongo.db.location.delete_many({})
        mongo.db.waterquality.delete_many({})

    def tearDown(self):
        pass  # Optionally, you can implement specific teardown actions per test if needed

    def test_add_and_get_admin(self):
        # Add an admin
        add_response = self.app.post('/admin', json={
            "name": "Test Admin",
            "email": "admin@test.com"
        })
        self.assertEqual(add_response.status_code, 201)
        admin_id = add_response.get_json()['id']

        # Get the admin
        get_response = self.app.get(f'/admin/{admin_id}')
        self.assertEqual(get_response.status_code, 200)
        admin = get_response.get_json()
        self.assertEqual(admin['name'], "Test Admin")
        self.assertEqual(admin['email'], "admin@test.com")

    def test_add_and_get_location(self):
        # Add a location
        add_response = self.app.post('/location', json={
            "name": "Test Location",
            "latitude": 40.7128,
            "longitude": -74.0060
        })
        self.assertEqual(add_response.status_code, 201)

        # Get all locations
        get_response = self.app.get('/location')
        self.assertEqual(get_response.status_code, 200)
        locations = get_response.get_json()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0]['name'], "Test Location")

    def test_add_get_update_delete_water_quality(self):
        # First, add a location
        location_response = self.app.post('/location', json={
            "name": "Test Location",
            "latitude": 40.7128,
            "longitude": -74.0060
        })
        location_id = location_response.get_json()['id']

        # Add water quality data
        add_response = self.app.post('/water_quality', json={
            "location_id": location_id,
            "ph": 7.5,
            "hardness": 150,
            "solids": 500,
            "chloramines": 5,
            "sulfate": 250,
            "conductivity": 500,
            "organic_carbon": 10,
            "trihalomethanes": 50,
            "turbidity": 5
        })
        self.assertEqual(add_response.status_code, 201)
        entry_id = add_response.get_json()['id']

        # Get the water quality entry
        get_response = self.app.get(f'/water_quality/{entry_id}')
        self.assertEqual(get_response.status_code, 200)
        entry = get_response.get_json()
        self.assertEqual(entry['ph'], 7.5)

        # Update the water quality entry
        update_response = self.app.put(f'/water_quality/{entry_id}', json={
            "location_id": location_id,
            "ph": 8.0,
            "hardness": 160,
            "solids": 550,
            "chloramines": 6,
            "sulfate": 260,
            "conductivity": 550,
            "organic_carbon": 11,
            "trihalomethanes": 55,
            "turbidity": 6
        })
        self.assertEqual(update_response.status_code, 200)

        # Verify the update
        get_response = self.app.get(f'/water_quality/{entry_id}')
        self.assertEqual(get_response.status_code, 200)
        updated_entry = get_response.get_json()
        self.assertEqual(updated_entry['ph'], 8.0)

        # Delete the water quality entry
        delete_response = self.app.delete(f'/water_quality/{entry_id}')
        self.assertEqual(delete_response.status_code, 200)

        # Verify the deletion
        get_response = self.app.get(f'/water_quality/{entry_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_invalid_add_admin_request(self):
        # Test invalid add admin request (missing required field 'email')
        add_response = self.app.post('/admin', json={"name": "Test Admin"})
        self.assertEqual(add_response.status_code, 400)

        # Ensure no admins were added
        get_response = self.app.get('/admin/' + str(ObjectId()))  # Using a dummy ID
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()