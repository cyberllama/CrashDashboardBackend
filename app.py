from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
from api.route.crash import crash_api
from api.route.image import image_api
from api.route.geojson import geojson_api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(home_api, url_prefix='/')
app.register_blueprint(crash_api, url_prefix='/crash')
app.register_blueprint(image_api, url_prefix='/image')
app.register_blueprint(geojson_api, url_prefix='/geojson')


# def create_app():
#     app = Flask(__name__)
#     CORS(app)

#     # app.config['SWAGGER'] = {
#     #     'title': 'Flask API Starter Kit',
#     # }
#     # swagger = Swagger(app)
#      ## Initialize Config
#     # app.config.from_pyfile('config.py')
#     app.register_blueprint(home_api, url_prefix='/')
#     app.register_blueprint(crash_api, url_prefix='/crash')
#     app.register_blueprint(image_api, url_prefix='/image')
#     app.register_blueprint(geojson_api, url_prefix='/geojson')


#     return app


# if __name__ == '__main__':
#     # from argparse import ArgumentParser

#     # parser = ArgumentParser()
#     # parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
#     # args = parser.parse_args()
#     # port = args.port

#     # app = create_app()

#     app.run()



    
