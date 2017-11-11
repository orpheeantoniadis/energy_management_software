#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from database import *

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

"""
@api {get} /:controller/:sensor/last_measure Request Sensor Last Measure
@apiName GetSensorLastMeasure
@apiGroup SensorsMeasures

@apiParam {int} controller Controller number
@apiParam {int} sensor Sensor id

@apiSuccess {int} humidity Humidity measured by the sensor
@apiSuccess {int} luminence  Luminence measured by the sensor
@apiSuccess {int} temperature  Temperature measured by the sensor
@apiSuccess {int} battery  Battery state of the sensor
@apiSuccess {date} date  Date of the measure
@apiSuccess {boolean} motion  Is the sensor in motion
"""
@app.route('/<int:controller>/<int:sensor>/last_measure', methods=['GET'])
def get_last_measure(controller, sensor):
	return jsonify(db.select_last_measure(controller, sensor))

"""
@api {get} /:room_id/average/:x Request Room Average x Measures
@apiName GetRoomAvgMeasures
@apiGroup RoomMeasures

@apiParam {int} room Room id
@apiParam {int} x Number of measures to take

@apiSuccess {float} humidity Humidity average in a room
@apiSuccess {float} luminence  Luminence average in a room
@apiSuccess {float} temperature  Temperature average in a room
"""
@app.route('/<string:room_id>/average/<int:x>', methods=['GET'])
def get_room_avg(room_id, x):
	return jsonify(db.select_room_avg(room_id, x))

"""
@api {get} /:controller/:sensor/:date1/:date2 Request Measures Between 2 Dates
@apiName GetMeasuresBetween
@apiGroup SensorsMeasures

@apiParam {int} controller Controller number
@apiParam {int} sensor Sensor id
@apiParam {int} date1 First date
@apiParam {int} date2 Second date

@apiSuccess {int} id Sensor id
@apiSuccess {String} controller  Controller name
@apiSuccess {int} humidity Humidity measured by the sensor
@apiSuccess {int} luminence  Luminence measured by the sensor
@apiSuccess {int} temperature  Temperature measured by the sensor
@apiSuccess {int} battery  Battery state of the sensor
@apiSuccess {date} date  Date of the measure
@apiSuccess {boolean} motion  Is the sensor in motion
"""
@app.route('/<int:controller>/<int:sensor>/<string:date1>/<string:date2>', methods=['GET'])
def get_measures_between(controller, sensor, date1, date2):
	return jsonify(db.select_measures_between(controller, sensor, date1, date2))

if __name__ == '__main__':
	db = database()
	app.run(debug=True)