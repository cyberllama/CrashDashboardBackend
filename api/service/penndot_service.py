import copy
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import List

from model.crash_point import CrashPoint

columns = defaultdict(list) # each value in each column is appended to a list

DEMOGRAPHIC_CATEGORIES = ["totpop2020", "hislat2020", "whitenh202", "blacknh202", "ainh2020", "asnh2020", "hipinh2020", "othernh202", "twoplsnh20"]

MODE_HIERARCHY = {
    "Pedestrian": 4,
    "Cyclist": 3,
    "Motorcyclist": 2,
    "Motorist": 1
}

SEVERITY_HIERARCHY = {
    "Fatality": 2,
    "Injury":  1
}

PEDESTRIAN_CATEGORIES = [
    "Pedestrian", "M/C and PED", "Pedestrian on scooter", "Ped on skateboard", "Scooter", "E-Scooter"
]

CYCLIST_CATEGORIES = [
    "Bicyclist", "Bicycle", "Bike"
]

MOTORCYCLIST_CATEGORIES = [
    "Motorcycle", "Dirt-bike", "M/C", "Dirtbike", "Quad", "Mini-bike", "Moped", "M/C and PED", "ATV"
]

MOTORIST_CATEGORIES = [
    "Auto", "Auto ", "Auto (Police)", "Van", "Tractor-Trailer", "School Bus", "Bus", "Truck", "Septa bus", "T/T", "Ambulance", "Tow truck"
]

OTHER_VEHICLES = [
    "Front-end loader", "Trolley car",  "Parked veh.", "Parked auto", "Parked TT",  "Parked autos", "Parked Trailer"
]

OTHER = [
    "Fixed Object", "unk", "Train", "Parked", "Tree", "None", "Ground", "Fixed object"
]

POSSIBLE_AUTO_CATEGORIES = MOTORIST_CATEGORIES + OTHER_VEHICLES + OTHER

def get_mode_hierarchy(incident_list):
    priority_incident = ()
    for incident in incident_list:
        if not priority_incident:
            priority_incident = incident
        else:
            if severity_hierarchy[incident[1]] > severity_hierarchy[priority_incident[1]]:
                priority_incident = incident
            elif severity_hierarchy[incident[1]] == severity_hierarchy[priority_incident[1]]:
                if(mode_hierarchy[incident[0]] > mode_hierarchy[priority_incident[0]]):
                    priority_incident = incident
    return priority_incident[0]

def get_crashes_by_year_range(from_year, to_year):
    crashes = []
    for year in range(from_year, to_year + 1):
        with open("./data/CRASH_PHILADELPHIA_{}.csv".format(year)) as f:
            reader = csv.DictReader(f) 
            for row in reader: 
                for (k,v) in row.items():
                    columns[k].append(v) 

                ped_death_total = int(row['PED_DEATH_COUNT'])
                bike_death_total = int(row['BICYCLE_DEATH_COUNT'])
                ped_inj_total = int(row["PED_SUSP_SERIOUS_INJ_COUNT"])
                bike_inj_total = int(row["BICYCLE_SUSP_SERIOUS_INJ_COUNT"])
                mcycle_death_total = int(row["MCYCLE_DEATH_COUNT"])
                mcycle_inj_total = int(row["MCYCLE_SUSP_SERIOUS_INJ_COUNT"])
                vehicle_death_total = int(row["FATAL_COUNT"]) - ped_death_total - bike_death_total - mcycle_death_total
                vehicle_inj_total = int(row["SUSP_SERIOUS_INJ_COUNT"]) - ped_inj_total - bike_inj_total - mcycle_inj_total

                total_deaths = ped_death_total + bike_death_total + vehicle_death_total + mcycle_death_total
                total_injuries = ped_inj_total + bike_inj_total + vehicle_inj_total + mcycle_inj_total
                total_incidents = total_deaths + total_injuries

                incident_list = []

                for x in range(ped_death_total):
                    incident_list.append(("Pedestrian", "Fatality"))
                for x in range(bike_death_total):
                    incident_list.append(("Cyclist", "Fatality"))
                for x in range(mcycle_death_total):
                    incident_list.append(("Motorcyclist", "Fatality"))
                for x in range(vehicle_death_total):
                    incident_list.append(("Motorist", "Fatality"))
                for x in range(ped_inj_total):
                    incident_list.append(("Pedestrian", "Injury"))
                for x in range(bike_inj_total):
                    incident_list.append(("Cyclist", "Injury"))
                for x in range(mcycle_inj_total):
                    incident_list.append(("Motorcyclist", "Injury"))
                for x in range(vehicle_inj_total):
                    incident_list.append(("Motorist", "Injury"))

                if(total_incidents > 0):
                    id = int(row['CRN'])
                    date = "{}-{}-01".format(row['CRASH_YEAR'], row['CRASH_MONTH'])
                    
                    # was breaking on some data point without coordinates, not sure what else to do here
                    point_x = 0
                    point_y = 0

                    if(row["DEC_LONG"] and row["DEC_LAT"]):
                        point_x = float(row["DEC_LONG"])
                        point_y = float(row["DEC_LAT"])
                        
                    year = int(date[0:4])
                    modes = []
                    if(ped_death_total + ped_inj_total > 0):
                        modes.append("Pedestrian")
                    if(bike_death_total + bike_inj_total > 0):
                        modes.append("Cyclist")
                    if(mcycle_death_total + mcycle_inj_total > 0):
                        modes.append("Motorcyclist")
                    if(vehicle_death_total + vehicle_inj_total > 0):
                        modes.append("Motorist")

                    max_severity = "Fatality" if total_deaths > 0 else "Injury"
                    mode_hierarchy = get_mode_hierarchy(incident_list)
                    category = mode_hierarchy + "_" + max_severity

                    crash = {
                        "id": id,
                        "date": date,
                        "year": year,
                        "point_x": point_x,
                        "point_y": point_y,
                        "max_severity": max_severity,
                        "most_affected_vulnerable_mode": mode_hierarchy,
                        "modes": modes,
                        "category": category.lower(),
                        "pedestrian_fatality_count": ped_death_total,
                        "pedestrian_injury_count": ped_inj_total,
                        "cyclist_fatality_count": bike_death_total,
                        "cyclist_injury_count": bike_inj_total,
                        "motorcyclist_fatality_count": mcycle_death_total,
                        "motorcyclist_injury_count": mcycle_inj_total,
                        "motorist_fatality_count": vehicle_death_total,
                        "motorist_injury_count": vehicle_inj_total,
                        "total_deaths": total_deaths,
                        "total_injuries": total_injuries,
                        "total_incidents": total_incidents,
                    }
                    
                    crashes.append(crash)
    return crashes



# Returns a CSV as a list of dicts
def csv_to_dicts(filepath: str) -> List[dict]:
    path = Path(filepath)
    with open (path, 'r') as file:
        return [d for d in csv.DictReader(file)]

# Filters a list of dicts to only include the given fields
def filter_for_fields(data: List[dict], *fields):
    filtered_data = []
    for entry in data:
        filtered_entry = {f: entry[f] for f in fields}
        filtered_data.append(filtered_entry)
    return filtered_data

def output_demographics_by_neighborhood():
    neighborhood_demographics = {}

    neighborhood_path = Path('data/neighborhoods.geojson')
    with open(neighborhood_path, 'r') as file:
        neighborhoods = json.load(file)

    initial_demographic_counts = {}
    for category in demographic_categories:
        initial_demographic_counts[category] = 0

    for feature in neighborhoods['features']:
        neighborhood_demographics[feature['properties']['name']] = copy.copy(initial_demographic_counts)
        
    tracts_to_neighborhood = get_tracts_by_neighborhood()
    data = csv_to_dicts('data/philly_2020_popdemographics_by_tract.csv')

    for row in data:
        tract_geoid = row['geoid']
        neighborhood = tracts_to_neighborhood[tract_geoid]
        
        for category in demographic_categories:
            neighborhood_demographics[neighborhood][category] += int(row[category])

    return neighborhood_demographics




        

    

    
