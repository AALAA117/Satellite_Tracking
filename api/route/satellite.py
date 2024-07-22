#!/usr/bin/python3
from api.route import main
from api.model.tle_fetcher import Satellite
from flask import abort, jsonify, request
from api.model import storage


@main.route("/active_sat/<name>", methods=["GET"], strict_slashes=False)
def get_sat(name):
    """
    Retrive expected position and velocity vector
    """
    if not name:
        abort(404)

    # check if satellite stored or not
    satellite = storage.get_sat(name)
    if not satellite:
        satellite = Satellite(name)
        norad_id = satellite.get_norad_id()
        tle_data = satellite.get_tle(norad_id)
        satellite.line_1 = tle_data[1].strip()
        satellite.line_2 = tle_data[2].strip()
        satellite.save()  # add new satellite to database
        storage.save()  # commit changes to database
    else:
        tle_data = [None, satellite.line_1, satellite.line_2]
    rv_data = satellite.predict_rv(tle_data)
    return(jsonify(rv_data))


@main.route("/active_sat/<name>", methods=["PUT"], strict_slashes=False)
def update_sat(name):
    """
    Update datetime of position and velocity vector
    """
    if not name:
        abort(404)

    # check if data is in json format
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    satellite = storage.get_sat(name)
    if not satellite:
        satellite = Base(name)
        norad_id = satellite.get_norad_id()
        tle_data = satellite.get_tle(norad_id)
        satellite.line_1 = tle_data[1].strip()
        satellite.line_2 = tle_data[2].strip()
    else:
        tle_data = [None, satellite.line_1, satellite.line_2]

    ignore = ["r_vector", "v_vector", "name"]
    # update date and time
    for key, value in data.items():
        if key not in ignore:
            setattr(satellite, key, value)
    rv_data = satellite.predict_rv(tle_data)
    return (jsonify(rv_data))
