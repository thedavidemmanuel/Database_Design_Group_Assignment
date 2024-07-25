import requests
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import json

# Suppress TensorFlow warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load the pretrained model
with open('water_quality_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# API base URL
BASE_URL = "http://localhost:5000"  # Adjust this if your API is hosted elsewhere

def get_water_quality_data():
    """Fetch water quality data from the API"""
    response = requests.get(f"{BASE_URL}/water_quality")
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response Headers: {json.dumps(dict(response.headers), indent=2)}")
    print(f"API Response Content: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}\nResponse content: {response.text}")

def prepare_data(data):
    """Prepare the data for prediction"""
    if not data:
        raise ValueError("The API returned an empty dataset")

    df = pd.DataFrame(data)
    print("Columns in the data:")
    print(df.columns)
    print("\nFirst few rows of the data:")
    print(df.head())

    # Select only the features used in training
    features = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate',
                'conductivity', 'organic_carbon', 'trihalomethanes', 'turbidity']

    # Check if all required features are present
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        raise ValueError(f"Missing features in the data: {missing_features}")

    X = df[features]

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled

def make_predictions(X):
    """Make predictions using the loaded model"""
    return model.predict(X)
