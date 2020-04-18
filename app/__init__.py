from flask_api import FlaskAPI
from flask import request, jsonify

import decimal
import flask.json

from app.models import HouseNany


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
        args = request.args
        results = HouseNany.get_schools(args)
        response = jsonify(results)
        response.data = flask.json.dumps(results).encode()
        response.status_code = 200
        return response

    # curl -X GET 'http://0.0.0.0:80/api/properties?schoolPostal=679676'
    @app.route("/api/properties", methods=['GET'])
    def get_properties_by_shool(*args, **kwargs):
        args = request.args
        results = HouseNany.get_properties(args)
        response = jsonify(results)
        response.data = flask.json.dumps(results).encode()
        response.status_code = 200
        return response

    # curl -X GET 'http://0.0.0.0:80/api/property?projectName=ESPA'
    @app.route("/api/property", methods=['GET'])
    def get_property():
        args = request.args
        results = HouseNany.get_property(args)
        response = jsonify(results)
        response.data = flask.json.dumps(results).encode()
        response.status_code = 200
        return response

    return app