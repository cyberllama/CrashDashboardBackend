from pathlib import Path

from flask import abort, request, send_file
from flask_api.status import *

from flask import Blueprint

image_api = Blueprint('image_api', __name__)

@image_api.route('/')
def get_image():
    name = request.args.get('type')
    root = Path(f'./api/images').resolve()
    file = (root / f'{name}.png').resolve()
    if not root.exists():
        return abort(HTTP_500_INTERNAL_SERVER_ERROR)
    if not str(file).startswith(str(root)):
        return abort(HTTP_403_FORBIDDEN)
    if not file.exists():
        return abort(HTTP_404_NOT_FOUND)
    return send_file(file, mimetype='image/png')
