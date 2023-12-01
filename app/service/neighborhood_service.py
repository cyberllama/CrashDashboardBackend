import json
from pathlib import Path

def get_preprocessed_neighborhood_geojson():
    path = Path('../data/neighborhoods.geojson')
    with open(path, 'r') as file:
        return json.load(file)