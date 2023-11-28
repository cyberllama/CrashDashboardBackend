import json
import urllib.request
from pathlib import Path

from flask import Flask, abort, request, send_file
from flask_api.status import *
from flask_cors import CORS
from utils.data_utils import *
from utils.geo_utils import *

app = Flask(__name__)
CORS(app)

baseUrl = "https://phl.carto.com/api/v2/"
ga = "2.159128115.869140587.1676312538-1066601619.1667858192"

@app.route("/opendataphilly")
def get_open_data_phily():
    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    fromDate += "-01-01"
    toDate += "-12-31"

    keyWords = "'Bike', 'Bicycle', 'Bicyclist', 'E-Bicycle', 'Pedestrian'"

    sql = "SELECT objectid, date_, primary_st, secondary_, age, veh1, veh2, point_x, point_y FROM fatal_crashes "
    # sql += "WHERE (veh1 IN ({}) OR veh2 IN ({}))".format(keyWords, keyWords)
    sql += "WHERE date_ >= '{}' AND date_ < '{}'".format(fromDate, toDate)

    url = baseUrl + "sql?q={}&_ga={}".format(sql, ga)
    print(url)

    url = url.replace(" ", "%20")

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    parsedData = convert_open_data_philly(dict["rows"])
    parsedData = find_and_add_neighborhoods(
        parsedData, get_coords=lambda x: (x['point_x'], x['point_y']))
    return parsedData

#TODO: remove other dupe
@app.route("/opendataphilly_geo")
def get_open_data_phily_geo():
    keyWords = "'Bike', 'Bicycle', 'Bicyclist', 'E-Bicycle', 'Pedestrian'"

    sql = "SELECT objectid, date_, primary_st, secondary_, age, veh1, veh2, point_x, point_y FROM fatal_crashes "

    url = baseUrl + "sql?q={}&_ga={}".format(sql, ga)
    print(url)

    url = url.replace(" ", "%20")

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    parsedData = convert_open_data_philly(dict["rows"])
    parsedData = find_and_add_neighborhoods(
        parsedData, get_coords=lambda x: (x['point_x'], x['point_y']))
    return create_feature_collection(parsedData)

@app.route("/penndot_geo")
def get_penndot_geo():
    # from_year = int(request.args.get('from'))
    # to_year = int(request.args.get('to'))
    # crashes = get_crashes_by_year_range(from_year, to_year)
    # crashes = find_and_add_neighborhoods(
    #     crashes, get_coords=lambda x: (x['point_x'], x['point_y']))
    # return create_feature_collection(crashes)
    path = Path('data/penndot_feature_collection.geojson')
    with open(path, 'r') as file:
        return json.load(file)

@app.route("/penndot")
def get_penndot():
    # from_year = int(request.args.get('from'))
    # to_year = int(request.args.get('to'))
    # crashes = get_crashes_by_year_range(from_year, to_year)
    # crashes = find_and_add_neighborhoods(
    #     crashes, get_coords=lambda x: (x['point_x'], x['point_y']))
    # return crashes
    path = Path('data/penndot_parsed.json')
    with open(path, 'r') as file:
        return json.load(file)

# @app.route("/penndot")
# def get_penndot():
#     # from_year = int(request.args.get('from'))
#     # to_year = int(request.args.get('to'))
#     # crashes = get_crashes_by_year_range(from_year, to_year)
#     # crashes = find_and_add_neighborhoods(
#     #     crashes, get_coords=lambda x: (x['point_x'], x['point_y']))
    
#     # return create_feature_collection(crashes)
#     path = Path('data/penndot_parsed.json')
#     with open(path, 'r') as file:
#         return json.load(file)

@app.route('/image')
def get_image():
    name = request.args.get('type')
    root = Path(f'images').resolve()
    file = (root / f'{name}.png').resolve()
    if not root.exists():
        return abort(HTTP_500_INTERNAL_SERVER_ERROR)
    if not str(file).startswith(str(root)):
        return abort(HTTP_403_FORBIDDEN)
    if not file.exists():
        return abort(HTTP_404_NOT_FOUND)
    return send_file(file, mimetype='image/png')

@app.route('/neighborhoods')
def get_neighborhoods():
    path = Path('data/neighborhoods.geojson')
    with open(path, 'r') as file:
        return json.load(file)
    

@app.route('/tracts')
def get_tracts():
    path = Path('data/tracts.geojson')
    with open(path, 'r') as file:
        return json.load(file)

FIELDS = [
    'PED_DEATH_COUNT',
    'BICYCLE_DEATH_COUNT',
    'CRASH_YEAR',
    'CRASH_MONTH',
    'DEC_LONG',
    'DEC_LAT',
]

# TODO: Match schema of existing crash endpoints.
@app.route('/crashes')
def get_crashes():
    data = csv_to_dicts('data/CRASH_PHILADELPHIA_2021.csv')
    data = filter_for_fields(data, *FIELDS)
    data = data[0:20]
    data = find_and_add_neighborhoods(
        data, get_coords=lambda x: (x['DEC_LONG'], x['DEC_LAT']))
    return data

@app.route('/demographics')
def get_demographics():
    data = output_demographics_by_neighborhood()
    return data



    
