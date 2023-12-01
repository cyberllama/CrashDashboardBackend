from flask import request 
from flask_api.status import *

from flask import Blueprint

from app.service.penndot_service import get_preprocessed_crashes
from app.service.opendataphilly_service import get_open_data_phily

crash_api = Blueprint('crash_api', __name__)

@crash_api.route('/penndot')
def get_penndot_crashes():
    #TODO: use sqlite db in place of preprocessed json
    result = get_preprocessed_crashes()
    return result, 200


@crash_api.route('/opendataphilly')
def get_opendataphilly_crashes():
    fromYear = request.args.get('from')
    toYear = request.args.get('to')
    result = get_open_data_phily(fromYear, toYear)
    return result, 200
