#!/usr/bin/python3
"""
Fetch TLE data from celestrack active satellites api
"""
import requests
from datetime import datetime
from pytz import timezone
from sgp4.api import Satrec, jday
from dotenv import load_dotenv
import os

load_dotenv()


class Base:
    def __init__(self, name):
        """
        initialization name and datetime
        """
        self.sat_name = name
        self.norad_id_url = os.getenv('NORAD_URL')
        self.tle_url = os.getenv('TLE_URL')
        self.date_time = None

    def get_norad_id(self):
        """
        return norad id
        """
        response = requests.get(self.norad_id_url)
        if response.status_code == 200:
            satellites = response.json()
            for satellite in satellites:
                if satellite["OBJECT_NAME"] == self.sat_name:
                    return(satellite["NORAD_CAT_ID"])
        else:
            return (None)
    def get_tle(self, norad_cat_id):
        """
        return tle data
        """
        url = "{}CATNR={}".format(self.tle_url, norad_cat_id)
        response = requests.get(url)
        if response.status_code == 200:
            tle_data = response.text.split("\r")
            return(tle_data)
        else:
            return (None)

    def predict_rv(self, tle_data):
        line1 = tle_data[1].strip()
        line2 = tle_data[2].strip()
        satellite = Satrec.twoline2rv(line1, line2)
        local_zone = timezone('Africa/Cairo')
        if self.date_time:
            date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            local_date_time = local_zone.localize(date_time)
            utc_time = local_date_time.astimezone(timezone('UTC'))
        else:
            utc_time = datetime.now(timezone('UTC'))

        year, month, day, hour, minute, sec = (
                utc_time.year, utc_time.month,
                utc_time.day, utc_time.hour,
                utc_time.minute, utc_time.second
                )
        julien_day, fr = jday(year, month, day, hour, minute, sec)
        e, r, v = satellite.sgp4(julien_day, fr)
        if e == 0:
            return ({
                "a_date": str(utc_time.date()),
                "a_time": str(utc_time.time()),
                "name": self.sat_name,
                "r_vector": {"x": r[0], "y": r[1], "z": r[2]},
                "v_vector": {"x": v[0], "y": v[1], "z": v[2]}
                })
        else:
            raise RuntimeError("Error")
