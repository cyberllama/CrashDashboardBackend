from pathlib import Path

from flask_api.status import *

from flask import Blueprint
from flasgger import swag_from
from app.model.welcome import WelcomeModel
from app.schema.welcome import WelcomeSchema

home_api = Blueprint('home_api', __name__)

@home_api.route('/')
def get_home():
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200