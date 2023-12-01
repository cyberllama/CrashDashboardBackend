from pathlib import Path

from flask import request
from flask_api.status import *
from flask import Blueprint

from app.service.geo_service import get_geojson_by_file_name, get_opendataphilly_geojson

geojson_api = Blueprint('geojson_api', __name__)

@geojson_api.route('/')
def get_geojson():
    file_name = request.args.get('name')
    result = {}
    if(file_name == "opendataphilly"):
        result = get_opendataphilly_geojson()
    else: 
        result = get_geojson_by_file_name(file_name)
    return result, 200