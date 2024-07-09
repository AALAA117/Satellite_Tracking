#!/usr/bin/python3
"""
Module for execution and handling error
"""
from flask import Flask, make_response, jsonify
from api.route import main
from os import environ


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    """handle 404 error

    Returns:
    Not found
    """
    return (make_response(jsonify({'error': 'Not found'}), 404))


if __name__ == '__main__':
    """Main Function"""
    host = environ.get('HOST')
    port = environ.get('PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5005
    app.run(debug=True, host=host, port=port)
