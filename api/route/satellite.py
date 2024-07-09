#!/usr/bin/python3
from api.route import main
from api.model.tle_fetcher import Base
from flask import abort, jsonify

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
