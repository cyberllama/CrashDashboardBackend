from flask_marshmallow import Schema
from marshmallow.fields import String, Integer, Date, Float, List

class CrashSchema(Schema):
    class Meta:
        id = Integer()
        date = Date()
        year = Integer()
        point_x = Float()
        max_severity = String()
        most_affected_vulnerable_mode = String()
        modes = List(String())
        category = String()
        pedestrian_fatality_count = Integer()
        pedestrian_injury_count = Integer()
        cyclist_fatality_count = Integer() 
        cyclist_injury_count = Integer()
        motorcyclist_fatality_count = Integer()
        motorcyclist_injury_count = Integer()
        motorist_fatality_count = Integer()
        motorist_injury_count = Integer()
        total_deaths = Integer()
        total_injuries = Integer()
        total_incidents = Integer()

crash_schema = CrashSchema()
crashes_schema = CrashSchema(many=True)

