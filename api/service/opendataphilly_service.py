import json
import urllib.request

from .geo_service import find_and_add_neighborhoods
from .consts import PEDESTRIAN_CATEGORIES, CYCLIST_CATEGORIES, MOTORCYCLIST_CATEGORIES, POSSIBLE_AUTO_CATEGORIES, OPENDATAPHILLY_BASE_URL, OPENDATAPHILLY_GA

def get_open_data_phily(from_year, to_year):
    fromDate = from_year + "-01-01"
    toDate = to_year + "-12-31"

    sql = "SELECT objectid, date_, primary_st, secondary_, age, veh1, veh2, point_x, point_y FROM fatal_crashes "
    sql += "WHERE date_ >= '{}' AND date_ < '{}'".format(fromDate, toDate)

    dict = query_open_data_philly(sql)
    parsedData = convert_open_data_philly(dict["rows"])
    parsedData = find_and_add_neighborhoods(
        parsedData, get_coords=lambda x: (x['point_x'], x['point_y']))
    return parsedData

def get_open_data_philly_report(from_year, to_year, modes):
    from_date = from_year + "-01-01"
    to_date = to_year + "-12-31"

    modes_to_query = []
    if "pedestrian" in modes:
        modes_to_query.append(PEDESTRIAN_CATEGORIES)
    if "cyclist" in modes:
        modes_to_query.append(CYCLIST_CATEGORIES)
    if "motorcyclist" in modes:
        modes_to_query.append(MOTORCYCLIST_CATEGORIES)
    if "motorist" in modes:
        modes_to_query.append(POSSIBLE_AUTO_CATEGORIES)

    modes_in_clause = ', '.join(['"{}"'.format(value) for value in modes_to_query])
    sql = "SELECT * FROM fatal_crashes "
    sql += "WHERE (date_ >= '{}' AND date_ < '{}') ".format(from_date, to_date)
    sql += f" AND (veh1 IN ({modes_in_clause}) OR veh2 IN ({modes_in_clause})"

    print(sql)
    dict = query_open_data_philly(sql)
    print(dict)

def query_open_data_philly(sql):
    url = OPENDATAPHILLY_BASE_URL + "sql?q={}&_ga={}".format(sql, OPENDATAPHILLY_GA)
    url = url.replace(" ", "%20")

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return dict

def convert_open_data_philly(data):
    crashes = []

    for row in data:
        pedTotal = 0
        bikeTotal = 0
        motorcycleTotal = 0
        motoristTotal = 0
        mode = ""

        veh1 = row['veh1']
        veh2 = row['veh2']

        if(veh1 in PEDESTRIAN_CATEGORIES or veh2 in PEDESTRIAN_CATEGORIES):
            pedTotal = 1
            mode = "Pedestrian"
        elif(veh1 in CYCLIST_CATEGORIES or veh2 in CYCLIST_CATEGORIES):
            bikeTotal = 1
            mode = "Cyclist"
        elif(veh1 in MOTORCYCLIST_CATEGORIES or veh2 in MOTORCYCLIST_CATEGORIES):
            motorcycleTotal = 1
            mode = "Motorcyclist"
        elif(veh1 in POSSIBLE_AUTO_CATEGORIES and veh2 in POSSIBLE_AUTO_CATEGORIES):
            motoristTotal = 1
            mode = "Motorist"

        date = row['date_'].split('T')[0]

        point_x = 0
        point_y = 0

        if(row['point_x'] and row['point_y']):
            point_x = float(row['point_x'])
            point_y = float(row['point_y'])

        category = mode + "_" + "fatality"
        totalDeaths = pedTotal + bikeTotal + motorcycleTotal + motoristTotal

        crash = {
            "id": row['objectid'],
            "date": date,
            "year": int(date[0:4]),
            "point_x": point_x,
            "point_y": point_y,
            "max_severity": "Fatality",
            "most_affected_vulnerable_mode": mode,
            "modes": [mode],
            "veh1": veh1,
            "veh2": veh2,
            "category": category.lower(),
            "pedestrian_fatality_count": pedTotal,
            "pedestrian_injury_count": 0,
            "cyclist_fatality_count": bikeTotal,
            "cyclist_injury_count": 0,
            "motorcyclist_fatality_count": motorcycleTotal,
            "motorcyclist_injury_count": 0,
            "motorist_fatality_count": motoristTotal,
            "motorist_injury_count": 0,
            "total_deaths": totalDeaths,
            "total_injuries": 0,
            "total_incidents": totalDeaths,
        }
        crashes.append(crash)
    return crashes

