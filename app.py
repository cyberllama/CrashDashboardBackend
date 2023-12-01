from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
from api.route.crash import crash_api
from api.route.image import image_api
from api.route.geojson import geojson_api
from flask_cors import CORS

def create_app():
    application = Flask(__name__)
    CORS(application)

     ## Initialize Config
    # app.config.from_pyfile('config.py')
    application.register_blueprint(home_api, url_prefix='/')
    application.register_blueprint(crash_api, url_prefix='/crash')
    application.register_blueprint(image_api, url_prefix='/image')
    application.register_blueprint(geojson_api, url_prefix='/geojson')


    return application


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    application = create_app()

    application.run(host='0.0.0.0', port=port)



    
