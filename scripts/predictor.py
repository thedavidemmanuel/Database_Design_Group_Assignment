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

