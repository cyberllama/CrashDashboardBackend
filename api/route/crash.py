from flask import request 
from flask_api.status import *
from flask import Blueprint, make_response
from datetime import date
from api.service.penndot_service import get_preprocessed_crashes, get_csv_from_qeury, construct_crash_query_from_filters
from api.service.opendataphilly_service import get_open_data_phily, get_open_data_philly_report

crash_api = Blueprint('crash_api', __name__)

@crash_api.route('/penndot')
def get_penndot_crashes():
    #TODO: use sqlite db in place of preprocessed json
    result = get_preprocessed_crashes()
    return result, 200


@crash_api.route('/opendataphilly')
def get_opendataphilly_crashes():
    from_year = request.args.get('from')
    to_year = request.args.get('to')
    result = get_open_data_phily(from_year, to_year)
    return result, 200

@crash_api.route('/report')
def get_crash_query_csv():
    from_year = request.args.get('from')
    to_year = request.args.get('to')
    modes = request.args.getlist('modes')
    severities = request.args.getlist('severities')

    query = construct_crash_query_from_filters(from_year, to_year, modes, severities)
    csv = get_csv_from_qeury(query)
    
    today = date.today()
    output = make_response(csv.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=crash_report_{today}.csv"
    output.headers["Content-type"] = "text/csv"
    return output
