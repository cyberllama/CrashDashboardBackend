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