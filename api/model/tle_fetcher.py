#!/usr/bin/python3
"""
Fetch TLE data from celestrack active satellites api
"""
import requests
import api.model
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pytz import timezone
from sgp4.api import Satrec, jday
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()


class Satellite(Base):
    """
    BaseModel for Satellites
    """
    __tablename__ = 'satellites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    line_1 = Column(String(70), nullable=False)
    line_2 = Column(String(70), nullable=False)
    # Define datetime cause it's an attribute for satellite
    # but we don't need to set a column for it
    date_time = None

    def __init__(self, name):
        """
        initialization name and datetime
        """
        self.name = name
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
                if satellite["OBJECT_NAME"] == self.name:
                    return(satellite["NORAD_CAT_ID"])
        else:
            return (None)

    # TLE data are two lines carry info
    # about satellite that we need to predict r and v
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
        """
        Predict Satellite Positin and Velocity
        in Km
        """
        # Prepare Tle data(two lines) and strip it from any space
        line1 = tle_data[1].strip()
        line2 = tle_data[2].strip()
        satellite = Satrec.twoline2rv(line1, line2)
        # timezone needed to determine r and v at greenwich timezone
        # according to our local timezone
        local_zone = timezone('Africa/Cairo')
        # for future date and time prediction
        if self.date_time:
            # take datetime in format '%Y-%m-%d %H:%M:%S'
            # and convert it to datetime object
            self.date_time = datetime.strptime(
                    self.date_time, '%Y-%m-%d %H:%M:%S'
                    )julien_day, fr = jday(year, month, day, hour, minute, sec)
            # set local time to the parsed date and time
            local_date_time = local_zone.localize(self.date_time)
            # change local time to greenwich time zone
            utc_time = local_date_time.astimezone(timezone('UTC'))
        else:
            utc_time = datetime.now(timezone('UTC'))

        year, month, day, hour, minute, sec = (
                utc_time.year, utc_time.month,
                utc_time.day, utc_time.hour,
                utc_time.minute, utc_time.second
                )
        julien_day, fr = jday(
                year, month, day, hour, minute, sec
                )  # convert to julien date
        e, r, v = satellite.sgp4(julien_day, fr)
        if e == 0:
            return ({
                "a_date": str(utc_time.date()),
                "a_time": str(utc_time.time()),
                "name": self.name,
                "r_vector (km)": {"x": r[0], "y": r[1], "z": r[2]},
                "v_vector (km/sec)": {"x": v[0], "y": v[1], "z": v[2]}
                })
        else:
            raise RuntimeError("Error")

    def save(self):
        """save object"""
        api.model.storage.new_sat(self)
