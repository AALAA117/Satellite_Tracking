#!/usr/bin/python3
"""
initialize the models package
"""
from api.model.db_storage import DBStorage
storage = DBStorage()
storage.reload()
