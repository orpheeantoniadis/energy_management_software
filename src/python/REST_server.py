#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import *
from database import *
from configparser import ConfigParser

app = Flask(__name__)

"""
@api {get} /controllers_list Controller List
@apiName GetControllerList
@apiGroup General

@apiExample {curl} Example usage:
curl -i http://localhost:5000/controllers_list

@apiSuccess {int} ip Controller ip address
@apiSuccess {str} name  Controller name
@apiSuccess {int} port Controller port

@apiSuccessExample {json} Success-Response:
[
  {
    "ip": "129.194.184.124",
    "name": "Pi 1",
    "port": 5000
  },
  {
    "ip": "129.194.184.125",
    "name": "Pi 2",
    "port": 5000
  },
  {
    "ip": "129.194.185.199",
    "name": "Pi 3",
    "port": 5000
  }
]
"""
@app.route('/controllers_list', methods=['GET'])
def get_all_controllers():
	return jsonify(db.select_all_controllers())

"""
@api {get} /:controller/sensors_list Sensors List
@apiName GetSensorsList
@apiGroup General

@apiExample {curl} Example usage:
curl -i http://localhost:5000/Pi%201/sensors_list

@apiParam {str} controller Controller name

@apiSuccess {int} controller Sensor's controller name
@apiSuccess {str} id Sensor unique id
@apiSuccess {int} location Location id

@apiSuccessExample {json} Success-Response:
[
  {
    "controller": "Pi 1",
    "id": 2,
    "location": "A501"
  },
  {
    "controller": "Pi 1",
    "id": 4,
    "location": "A502"
  }
]
"""
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

@apiExample {curl} Example usage:
curl -i http://localhost:5000/Pi%201/2/last_measures

@apiParam {str} controller Controller name
@apiParam {int} sensor Sensor id

@apiSuccess {int} id Sensor id
@apiSuccess {str} controller  Controller name
@apiSuccess {int} humidity Humidity measured by the sensor
@apiSuccess {int} luminence  Luminence measured by the sensor
@apiSuccess {int} temperature  Temperature measured by the sensor
@apiSuccess {int} battery  Battery state of the sensor
@apiSuccess {date} date  Date of the measure
@apiSuccess {boolean} motion  Is the sensor in motion

@apiSuccessExample {json} Success-Response:
[
  {
    "battery": 23,
    "controller": "Pi 1",
    "date": "Mon, 20 Nov 2017 11:02:00 GMT",
    "humidity": 27,
    "id": 2,
    "luminance": 172,
    "motion": true,
    "temperature": 23
  }
]
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

@apiExample {curl} Example usage:
curl -i http://localhost:5000/A432/average/5

@apiParam {int} room Room id
@apiParam {int} x Number of measures to take

@apiSuccess {str} room Room id
@apiSuccess {float} humidity Humidity average in a room
@apiSuccess {float} luminence  Luminence average in a room
@apiSuccess {float} temperature  Temperature average in a room

@apiSuccessExample {json} Success-Response:
[
  {
    "humidity": 20.0,
    "luminance": 130.4,
    "room": "A432",
    "temperature": 27.4
  }
]
"""
@app.route('/<string:room_id>/average/<int:x>', methods=['GET'])
def get_room_avg(room_id, x):
	flag = False
	rooms = db.select_all_rooms()
	for room in rooms:
		if room == room_id:
			flag = True
	if flag == False:
		return 'Sorry, wrong room !'
	nbr = db.select_nbr_measures_room(room_id)
	if x > nbr:
		return 'Sorry, there is just '+str(nbr)+' measures for this room'
	return jsonify(db.select_room_avg(room_id, x))

"""
@api {get} /:controller/:sensor/:date1/:date2 Measures Between 2 Dates
@apiName GetMeasuresBetween
@apiGroup SensorsMeasures

@apiExample {curl} Example usage:
curl -i http://localhost:5000/Pi%201/2/2017-11-15%2008:24:30/2017-11-15%2009:36:30

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

@apiSuccessExample {json} Success-Response:
[
  {
    "battery": 29,
    "controller": "Pi 1",
    "date": "Wed, 15 Nov 2017 08:24:30 GMT",
    "humidity": 23,
    "id": 2,
    "luminance": 163,
    "motion": false,
    "temperature": 21
  },
  {
    "battery": 29,
    "controller": "Pi 1",
    "date": "Wed, 15 Nov 2017 08:28:30 GMT",
    "humidity": 23,
    "id": 2,
    "luminance": 176,
    "motion": false,
    "temperature": 21
  },
  {
    "battery": 29,
    "controller": "Pi 1",
    "date": "Wed, 15 Nov 2017 09:36:30 GMT",
    "humidity": 22,
    "id": 2,
    "luminance": 1000,
    "motion": false,
    "temperature": 22
  }
]
"""
@app.route('/<string:controller>/<int:sensor>/<string:date1>/<string:date2>', methods=['GET'])
def get_measures_between(controller, sensor, date1, date2):
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
	app.run(debug=True,host=ip[1])
