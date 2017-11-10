#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from database import *

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/<int:controller>/<int:sensor>/last_measure', methods=['GET'])
def get_last_measure(controller, sensor):
	return jsonify({'last_measures': db.select_last_measure(controller, sensor)})


if __name__ == '__main__':
	db = database()
	app.run(debug=True)