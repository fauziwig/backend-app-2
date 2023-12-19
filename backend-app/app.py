from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load dataset
data = pd.read_csv("WarungDataset.csv")
coordinates = data[["Latitude", "Longitude"]].values

# Normalization of coordinates
scaler = StandardScaler()
normalized_coordinates = scaler.fit_transform(coordinates)

# Function to calculate Haversine distance
def haversine_distance(lon1, lat1, lon2, lat2):
    R = 6371.0  # Earth radius in kilometers

    lon1_rad = np.radians(lon1)
    lat1_rad = np.radians(lat1)
    lon2_rad = np.radians(lon2)
    lat2_rad = np.radians(lat2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

# Calculate Haversine distance from new coordinates to all data points
def calculate_recommendations(new_longitude, new_latitude, k=3):
    distances = haversine_distance(data["Longitude"].values, data["Latitude"].values, new_longitude, new_latitude)

    # Find nearest neighbors
    nearest_neighbors_indices = np.argsort(distances)[:k]

    # Get recommendations based on nearest neighbors found
    recommendations = data.iloc[nearest_neighbors_indices]["Nama Warung"].tolist()
    
    return recommendations

# Define an API endpoint for getting recommendations based on new coordinates using GET
@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    # Example input longitude and latitude
    new_longitude = float(request.args.get('longitude', -7.82484))
    new_latitude = float(request.args.get('latitude', 110.379357))
    
    # Calculate recommendations
    recommendations = calculate_recommendations(new_longitude, new_latitude)
    
    return jsonify({"recommendations": recommendations})

# Define an API endpoint for Haversine distance calculation
@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    data = request.get_json()

    lon1 = data['lon1']
    lat1 = data['lat1']
    lon2 = data['lon2']
    lat2 = data['lat2']

    distance = haversine_distance(lon1, lat1, lon2, lat2)

    response = {'distance': distance}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
