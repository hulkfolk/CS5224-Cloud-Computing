from flask_api import FlaskAPI
from flask import request, jsonify

import json

from app.models import HouseNany


def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    @app.route('/housenany/service/getschools', methods=['GET'])
    def get_schools():
        results = HouseNany.get_schools()
        response = jsonify(results)
        response.data = json.dumps(results).encode()
        response.status_code = 200
        return response

    # /housenany/service/getproperties/?school=
    # curl -X GET 'http://0.0.0.0:80/housenany/service/getproperties/?school=school1'
    @app.route("/housenany/service/getproperties/", methods=['GET'])
    def get_properties_by_shool(*args, **kwargs):
        if "school" in request.args:
            school = request.args["school"]
            results = HouseNany.get_properties(school)
            response = jsonify(results)
            response.data = json.dumps(results).encode()
            response.status_code = 200
            return response

    return app