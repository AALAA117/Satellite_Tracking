#!/usr/bin/python3
"""
Fetch TLE data from Celestrak active satellites API
"""
import requests
from datetime import datetime
from pytz import timezone
from sgp4.api import Satrec, jday


class Base:
    def __init__(self, name):
        """
        Initialization name and datetime
        """
        self.sat_name = name

    def get_norad_id(self):
        """
        Return NORAD ID
        """
        url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
        response = requests.get(url)
        if response.status_code == 200:
            satellites = response.json()
            for satellite in satellites:
                if satellite["OBJECT_NAME"] == self.sat_name:
                    return satellite["NORAD_CAT_ID"]
        return None

    def get_tle(self, norad_cat_id):
        """
        Return TLE data
        """
        url = "https://celestrak.org/NORAD/elements/gp.php?CATNR={}".format(norad_cat_id)
        response = requests.get(url)
        if response.status_code == 200:
            tle_data = response.text.split("\r")
            return tle_data
        else:
            return None

    def predict_rv(self, tle_data):
        line1 = tle_data[1].strip()
        line2 = tle_data[2].strip()
        satellite = Satrec.twoline2rv(line1, line2)
        utc_time = datetime.now(timezone('UTC'))
        year, month, day, hour, minute, sec = (
            utc_time.year, utc_time.month, utc_time.day,
            utc_time.hour, utc_time.minute, utc_time.second
        )
        julian_day, fr = jday(year, month, day, hour, minute, sec)
        e, r, v = satellite.sgp4(julian_day, fr)
        if e == 0:
            return ({
                "r_vector": {"x": r[0], "y": r[1], "z": r[2]},
                "v_vector": {"x": v[0], "y": v[1], "z": v[2]}
                })
        else:
            print(f"SGP4 error code: {e}")
            print("TLE data might be invalid or there is an issue with the SGP4 calculation.")
            print(f"Line 1: {line1}")
            print(f"Line 2: {line2}")
            raise RuntimeError("Error calculating satellite position and velocity")


def main():
    sat_name = input("Enter the satellite name: ")
    satellite = Base(sat_name)
    
    norad_id = satellite.get_norad_id()
    if norad_id:
        tle_data = satellite.get_tle(norad_id)
        if tle_data:
            try:
                rv_data = satellite.predict_rv(tle_data)
                print("Position Vector:", rv_data["r_vector"])
                print("Velocity Vector:", rv_data["v_vector"])
            except RuntimeError as e:
                print(e)
        else:
            print("Failed to fetch TLE data.")
    else:
        print("Failed to fetch NORAD ID.")


if __name__ == "__main__":
    main()

