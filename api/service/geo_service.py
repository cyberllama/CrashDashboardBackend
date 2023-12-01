import json
import datetime
from pathlib import Path
from typing import List

from geojson import Feature, FeatureCollection, Point
from shapely.geometry import Point, shape

def get_geojson_by_file_name(file_name):
    path = Path(f'./api/data/geojson/{file_name}.geojson')
    print(path)
    with open(path, 'r') as file:
        return json.load(file)
    
def get_opendataphilly_geojson():
    from api.service.opendataphilly_service import get_open_data_phily
    currentYear = datetime.date.today().year
    crashes = get_open_data_phily("2019", str(currentYear))
    return create_feature_collection(crashes)

def create_feature_collection(crashes):
    crash_features = []
    for crash in crashes:
        point = Point((crash['point_x'], crash['point_y']))
        feature = Feature(geometry=point, id=crash['id'], properties=crash)
        crash_features.append(feature)
    return FeatureCollection(crash_features)

def find_and_add_neighborhoods(
        crashes: List[dict],
        get_coords=None) -> List[dict]:
    path = Path(f'./api/data/geojson/neighborhoods.geojson')
    with open(path, 'r') as file:
        neighborhoods = json.load(file)

    def _find_name(lat, long) -> str:
        try:
            lat = float(lat)
            long = float(long)
            point = Point(lat, long)
        except:
            return "INVALID"

        def _arbitrary_border_point(neighborhood) -> Point:
            return Point(neighborhood['geometry']['coordinates'][0][0][0])

        neighborhoods['features'].sort(
            key=lambda x: _arbitrary_border_point(x).distance(point))

        for feature in neighborhoods['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return feature['properties']['name']
        return "UNKNOWN"

    for crash in crashes:
        lat, long = get_coords(crash)
        name = _find_name(lat, long)
        crash['neighborhood'] = name

    return crashes

def get_tracts_by_neighborhood():
    neighborhood_path = Path(f'./api/data/neighborhoods.geojson')
    with open(neighborhood_path, 'r') as file:
        neighborhoods = json.load(file)

    tracts_path = Path(f'./api/data/tracts.geojson')
    with open(tracts_path, 'r') as file:
        tracts = json.load(file)

    tract_centroid_dict = {}
    for feature in tracts['features']:
        polygon = shape(feature['geometry'])
        centroid = polygon.centroid
        geoid = feature['properties']['geoid']
        tract_centroid_dict[geoid] = centroid


    tract_to_neighborhood_dict = {}
    for key, value in tract_centroid_dict.items():
        for feature in neighborhoods['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(value):
                tract_to_neighborhood_dict[key] = feature['properties']['name']

    return tract_to_neighborhood_dict