from flask_api import FlaskAPI
from flask import request, jsonify

import decimal
import flask.json

from app.models import HouseNany
from data.db_controller import get_logger

logger = get_logger()


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return float(obj)
        return super(MyJSONEncoder, self).default(obj)


def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    app.json_encoder = MyJSONEncoder

    # curl -X GET 'http://0.0.0.0:80/api/schools?name=tec&mrt=ang%20mo%20kio$chua%20chu&lang=chinese&offering=media$tgps'
    @app.route('/api/schools', methods=['GET'])
    def get_schools():
        logger.info(request.url)
        args = request.args
        results = HouseNany.get_schools(args)
        response = jsonify(results)
        response.data = flask.json.dumps(results).encode()
        response.status_code = 200
        logger.info(response.status_code)
        return response

    # curl -X GET 'http://0.0.0.0:80/api/properties?schoolPostal=679676'
    @app.route("/api/properties", methods=['GET'])
    def get_properties_by_shool(*args, **kwargs):
        logger.info(request.url)
        args = request.args
        results = HouseNany.get_properties(args)
        response = jsonify(results)
        response.data = flask.json.dumps(results).encode()
        response.status_code = 200
        logger.info(response.status_code)
        return response

    # curl -X GET 'http://0.0.0.0:80/api/property?projectName=CUSCADEN%20RESERVE'
    @app.route("/api/property", methods=['GET'])
    def get_property():
        logger.info(request.url)
        args = request.args
        results = HouseNany.get_property(args)
        response = jsonify(results)
        response.data = flask.json.dumps(results).encode()
        response.status_code = 200
        logger.info(response.status_code)
        return response

    return app