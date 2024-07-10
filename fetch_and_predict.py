import requests
import numpy as np
import tensorflow as tf
from tensorflow import keras

# API endpoint
API_URL = "http://localhost:5000/waterquality"

def fetch_latest_entry():
    """Fetch the latest water quality entry from the API"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        entries = response.json()
        if entries:
            return entries[-1]  # Return the last (latest) entry
    return None

def prepare_data(entry):
    """Prepare the input data for prediction"""
    features = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate',
                'conductivity', 'organic_carbon', 'trihalomethanes', 'turbidity']

    input_data = [entry.get(feature, 0) for feature in features]
    return np.array([input_data])

def make_prediction(model, input_data):
    """Use the model to make a prediction"""
    prediction = model.predict(input_data)
    return prediction[0][0]  # Assuming binary classification (0 or 1)

def main():
    # Fetch the latest entry
    latest_entry = fetch_latest_entry()
    if not latest_entry:
        print("Failed to fetch the latest water quality entry.")
        return

    # Prepare the input data
    input_data = prepare_data(latest_entry)

    # Load the model
    model = load_model()

    # Make a prediction
    prediction = make_prediction(model, input_data)

    # Print the results
    print("Latest Water Quality Data:")
    print(f"Location ID: {latest_entry.get('location_id', 'N/A')}")
    print(f"Timestamp: {latest_entry.get('timestamp', 'N/A')}")
    print("\nWater Quality Parameters:")
    for key, value in latest_entry.items():
        if key not in ['_id', 'location_id', 'timestamp']:
            print(f"{key}: {value}")

    print(f"\nPrediction: {'Potable' if prediction > 0.5 else 'Not Potable'}")
    print(f"Confidence: {prediction:.2%}")

if __name__ == "__main__":
    main()

