import copy
import json
from pathlib import Path

from consts import  DEMOGRAPHIC_CATEGORIES
from utils import csv_to_dicts
from geo_service import get_tracts_by_neighborhood

def get_neighborhood_demographics():
    neighborhood_demographics = {}

    neighborhood_path = Path('data/neighborhoods.geojson')
    with open(neighborhood_path, 'r') as file:
        neighborhoods = json.load(file)

    initial_demographic_counts = {}
    for category in DEMOGRAPHIC_CATEGORIES:
        initial_demographic_counts[category] = 0

    for feature in neighborhoods['features']:
        neighborhood_demographics[feature['properties']['name']] = copy.copy(initial_demographic_counts)
        
    tracts_to_neighborhood = get_tracts_by_neighborhood()
    data = csv_to_dicts('data/philly_2020_popdemographics_by_tract.csv')

    for row in data:
        tract_geoid = row['geoid']
        neighborhood = tracts_to_neighborhood[tract_geoid]
        
        for category in DEMOGRAPHIC_CATEGORIES:
            neighborhood_demographics[neighborhood][category] += int(row[category])

    return neighborhood_demographics