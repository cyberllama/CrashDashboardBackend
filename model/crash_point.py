from marshmallow import Schema, fields


class CrashPoint(object):
    def __init__(self, id, date, ped_death_total, bicycle_death_total, point_x, point_y):
        self.id = id
        self.date = date
        self.ped_death_total = ped_death_total
        self.bicycle_death_total = bicycle_death_total
        self.point_x = point_x
        self.point_y = point_y

class CrashPoint(Schema):
    id: fields.String()
    date: fields.Date()
    ped_death_total: fields.Number()
    bicycle_death_total: fields.Number()
    point_x: fields.Float
    point_y: fields.Float