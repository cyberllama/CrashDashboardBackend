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

OPENDATAPHILLY_BASE_URL = "https://phl.carto.com/api/v2/"
OPENDATAPHILLY_GA = "2.159128115.869140587.1676312538-1066601619.1667858192"

OPENDATAPHILLY_FIELDS = [
    "cartodb_id", "the_geom", "the_geom_webmercator", "objectid", "year", "district", "dc_number", "date_", "primary_st", "secondary_", "age",
    "sex", "crash_type" , "hit_____ru", "veh1", "veh2", "arrest_yes", "investigat", "dc_key", "point_x", "point_y"
]

MODE_SEVERITY_FIELD_MAPPING = {
    ("pedestrian", "fatality"): "PED_DEATH_COUNT",
    ("pedestrian", "injury"): "PED_SUSP_SERIOUS_INJ_COUNT",
    ("cyclist", "fatality"): "BICYCLE_DEATH_COUNT",
    ("cyclist", "injury"): "BICYCLE_SUSP_SERIOUS_INJ_COUNT",
    ("motorcyclist", "fatality"): "MCYCLE_DEATH_COUNT",
    ("motorcyclist", "injury"): "MCYCLE_SUSP_SERIOUS_INJ_COUNT",
    ("motorist", "fatality"): "(FATAL_COUNT - PED_DEATH_COUNT - BICYCLE_DEATH_COUNT - MCYCLE_DEATH_COUNT)",
    ("motorist", "injury"): "(SUSP_SERIOUS_INJ_COUNT - PED_SUSP_SERIOUS_INJ_COUNT - BICYCLE_SUSP_SERIOUS_INJ_COUNT - MCYCLE_SUSP_SERIOUS_INJ_COUNT)"
}

