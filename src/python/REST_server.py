#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import *
from flask_restful import *
from flask import render_template
from database import *
from configparser import ConfigParser

app = Flask(__name__)
api = Api(app)

@app.route('/controllers_list', methods=['GET'])
def get_all_controllers():
	return jsonify(db.select_all_controllers())

@app.route('/<string:controller>/sensors_list', methods=['GET'])
def get_all_sensors(controller):
	flag = False
	# check if <controller> exists
	controllers = db.select_all_controllers()
	for cont in controllers:
		if cont.get('name') == controller:
			flag = True

	if flag == True:
		return jsonify(db.select_all_sensors(controller))

	return 'Sorry, wrong controller !'

"""
@api {get} /:controller/:sensor/last_measures Sensor Last Measures
@apiName GetSensorLastMeasures
@apiGroup SensorsMeasures

@apiParam {int} controller Controller number
@apiParam {int} sensor Sensor id

@apiSuccess {int} id Sensor id
@apiSuccess {str} controller  Controller name
@apiSuccess {int} humidity Humidity measured by the sensor
@apiSuccess {int} luminence  Luminence measured by the sensor
@apiSuccess {int} temperature  Temperature measured by the sensor
@apiSuccess {int} battery  Battery state of the sensor
@apiSuccess {date} date  Date of the measure
@apiSuccess {boolean} motion  Is the sensor in motion
"""
@app.route('/<string:controller>/<int:sensor>/last_measures', methods=['GET'])
def get_last_measures(controller, sensor):
	flag = False
	# check if controller exists
	controllers = db.select_all_controllers()
	for cont in controllers:
		if cont.get('name') == controller:
			flag = True
	if flag == False:
		return 'Sorry, wrong controller !'

	# check if the sensor exists
	flag = False
	sensors = db.select_all_sensors(controller)
	for sens in sensors:
		if sens.get('id') == sensor:
			flag = True
	if flag == False:
		return 'Sorry, wrong sensor !'

	return jsonify(db.select_last_measures(controller, sensor))

"""
@api {get} /:room_id/average/:x Room Average x Measures
@apiName GetRoomAvgMeasures
@apiGroup RoomMeasures

@apiParam {int} room Room id
@apiParam {int} x Number of measures to take

@apiSuccess {str} room Room id
@apiSuccess {float} humidity Humidity average in a room
@apiSuccess {float} luminence  Luminence average in a room
@apiSuccess {float} temperature  Temperature average in a room
"""
@app.route('/<string:room_id>/average/<int:x>', methods=['GET'])
def get_room_avg(room_id, x):
	return jsonify(db.select_room_avg(room_id, x))

"""
@api {get} /:controller/:sensor/:date1/:date2 Measures Between 2 Dates
@apiName GetMeasuresBetween
@apiGroup SensorsMeasures

@apiParam {str} controller Controller number
@apiParam {int} sensor Sensor id
@apiParam {int} date1 First date
@apiParam {int} date2 Second date

@apiSuccess {int} id Sensor id
@apiSuccess {str} controller  Controller name
@apiSuccess {int} humidity Humidity measured by the sensor
@apiSuccess {int} luminence  Luminence measured by the sensor
@apiSuccess {int} temperature  Temperature measured by the sensor
@apiSuccess {int} battery  Battery state of the sensor
@apiSuccess {date} date  Date of the measure
@apiSuccess {boolean} motion  Is the sensor in motion
"""
@app.route('/<string:controller>/<int:sensor>/<string:date1>/<string:date2>', methods=['GET'])
def get_measures_between(controller, sensor, date1, date2):
	return jsonify(db.select_measures_between(controller, sensor, date1, date2))


if __name__ == '__main__':
	db = database()
	parser = ConfigParser()
	parser.read('rest_server.ini')
	if parser.has_section('rest_server'):
		params = parser.items('rest_server')
		ip = params[0]
	else:
		raise Exception('Section {0} not found in the {1} file'.format(section, filename))
	#api = Api(app, errors=errors)
	app.run(debug=True,host=ip[1])
