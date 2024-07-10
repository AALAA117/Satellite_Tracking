#!/usr/bin/python3
from api.route import main
from api.model.tle_fetcher import Base
from flask import abort, jsonify, request

@main.route("/active_sat/<name>", methods=["GET"], strict_slashes=False)
def get_sat(name):
    """
    Retrive expected position and velocity vector
    """
    if not name:
        abort(404)

    satellite = Base(name)
    norad_id = satellite.get_norad_id()
    tle_data = satellite.get_tle(norad_id)
    rv_data = satellite.predict_rv(tle_data)
    return(jsonify(rv_data))

@main.route("/active_sat/<name>", methods=["PUT"], strict_slashes=False)
def update_sat(name):
    """
    Update datetime of position and velocity vector
    """
    satellite = Base(name)
    norad_id = satellite.get_norad_id()
    tle_data = satellite.get_tle(norad_id)
    if name:
        if not request.get_json():
            abort(400, description="Not a JSON")

        data = request.get_json()
        ignore = ["r_vector", "v_vector", "name", "date_time"]
        for key, value in data.items():
            if key not in ignore:
                setattr(satellite, key, value)
        rv_data = satellite.predict_rv(tle_data)
        return (jsonify(rv_data))
    else:
        abort(404)
