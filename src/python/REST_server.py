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
	return jsonify({'measures': db.select_last_measure(controller, sensor)})

@app.route('/<string:room_id>/average/<int:x>', methods=['GET'])
def get_room_avg(room_id, x):
	return jsonify({'measures': db.select_room_avg(room_id, x)})

@app.route('/<int:controller>/<int:sensor>/<string:date1>/<string:date2>', methods=['GET'])
def get_measures_between(controller, sensor, date1, date2):
	return jsonify({'measures': db.select_measures_between(controller, sensor, date1, date2)})

if __name__ == '__main__':
	db = database()
	app.run(debug=True)