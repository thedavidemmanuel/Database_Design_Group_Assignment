import unittest
from app import app, mongo

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

        # Get all admins
        get_response = self.app.get('/admin')
        self.assertEqual(get_response.status_code, 200)
        admins = get_response.get_json()
        self.assertEqual(len(admins), 1)
        self.assertEqual(admins[0]['name'], "Test Admin")

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

    def test_add_and_get_water_quality(self):
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

        # Get all water quality entries
        get_response = self.app.get('/water_quality')
        self.assertEqual(get_response.status_code, 200)
        entries = get_response.get_json()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['ph'], 7.5)

    def test_predict(self):
        # Add a location
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

        # Get prediction
        prediction_response = self.app.get('/predict')
        self.assertEqual(prediction_response.status_code, 200)
        prediction_data = prediction_response.get_json()
        self.assertIn('prediction', prediction_data)
        self.assertIn('confidence', prediction_data)

    def test_invalid_add_admin_request(self):
        # Test invalid add admin request (missing required field 'email')
        add_response = self.app.post('/admin', json={"name": "Test Admin"})
        self.assertEqual(add_response.status_code, 400)

        # Ensure no admins were added
        get_response = self.app.get('/admin')
        self.assertEqual(get_response.status_code, 200)
        admins = get_response.get_json()
        self.assertEqual(len(admins), 0)

if __name__ == '__main__':
    unittest.main()
