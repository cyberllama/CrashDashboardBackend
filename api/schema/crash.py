from flask_marshmallow import Schema
from marshmallow.fields import Str


class CrashSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "date", "year", "point_x", "point_y", "max_severity", 
        "most_affected_vulnerable_mode", "modes", "category", "pedestrian_fatality_count", 
        "pedestrian_injury_count", "cyclist_fatality_count", "cyclist_injury_count", "motorcyclist_fatality_count", "motorcyclist_injury_count", 
        "motorist_fatality_count": , "motorist_injury_count":, "total_deaths":, "total_injuries": "total_incidents"]

    message = Str()

crash_schema = CrashSchema()
crashes_schema = CrashSchema(many=True)

