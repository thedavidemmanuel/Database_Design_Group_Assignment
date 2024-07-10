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

