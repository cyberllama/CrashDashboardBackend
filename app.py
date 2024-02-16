from datetime import date
from flask import Flask, make_response, request
from flask_caching import Cache
from flask_cors import CORS

import time
from api.service.geo_service import get_geojson_by_file_name, get_opendataphilly_geojson
from api.service.opendataphilly_service import get_open_data_phily

from api.service.penndot_service import construct_crash_query_from_filters, get_csv_from_qeury, get_preprocessed_crashes

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)


@app.route('/crash/penndot')
def get_penndot_crashes():
    result = get_preprocessed_crashes()
    return result, 200


@cache.cached(timeout=600)
@app.route('/crash/opendataphilly')
def get_opendataphilly_crashes():
    start_time = time.time()
    from_year = request.args.get('from')
    to_year = request.args.get('to')
    result = get_open_data_phily(from_year, to_year)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"retrieved in {elapsed_time:.4f} seconds")
    return result, 200

@app.route('/crash/report')
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

@app.route('/geojson/')
def get_geojson():
    file_name = request.args.get('name')
    result = {}
    if(file_name == "opendataphilly"):
        result = get_opendataphilly_geojson()
    else: 
        result = get_geojson_by_file_name(file_name)
    return result, 200

if __name__ == '__main__': 
    app.run(debug=True)

    
