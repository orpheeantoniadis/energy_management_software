#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import *
from database import *
from configparser import ConfigParser
import requests

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

@apiError ControllerNotFound The <code>name</code> of the Controller was not found.

@apiErrorExample {json} Error-Response:
{
      "error": "ControllerNotFound"
}
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

	return jsonify({'error':'ControllerNotFound'})

"""
@api {get} /rooms_list Rooms List
@apiName GetRoomsList
@apiGroup General

@apiExample {curl} Example usage:
curl -i http://localhost:5000/rooms_list

@apiSuccess {str[]} rooms Array of room ids

@apiSuccessExample {json} Success-Response:
{
  "rooms": [
    "A400",
    "A401",
    "A402",
    "A403",
    "A404",
    "A406",
    "A432"
  ]
}
"""
@app.route('/rooms_list', methods=['GET'])
def get_all_rooms():
	return jsonify({'rooms':db.select_all_rooms()})

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

@apiError ControllerNotFound The <code>name</code> of the Controller was not found.
@apiError SensorNotFound The <code>id</code> of the Sensor was not found.

@apiErrorExample {json} Error-Response:
{
	"error": "ControllerNotFound"
}
@apiErrorExample {json} Error-Response:
{
	"error": "SensorNotFound"
}
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
        return jsonify({'error':'ControllerNotFound'})

    # check if the sensor exists
    flag = False
    sensors = db.select_all_sensors(controller)
    for sens in sensors:
        if sens.get('id') == sensor:
            flag = True
    if flag == False:
        return jsonify({'error':'SensorNotFound'})

    return jsonify(db.select_last_measures(controller, sensor))
"""
@api {get} /:room_id/nbMeasures Room Number of Measures
@apiName GetRoomNbMeasures
@apiGroup RoomMeasures

@apiExample {curl} Example usage:
curl -i http://localhost:5000/A432/nbMeasures

@apiParam {int} room Room id

@apiSuccess {int} nbMeasures Number of measures

@apiSuccessExample {json} Success-Response:
{
  "nbMeasures": 234
}

@apiError RoomNotFound The <code>id</code> of the Room was not found.

@apiErrorExample {json} Error-Response:
{
    "error": "RoomNotFound"
}

"""
@app.route('/<string:room_id>/nbMeasures', methods=['GET'])
def get_room_nbMeasures(room_id):
    flag = False
    rooms = db.select_all_rooms()
    for room in rooms:
        if room == room_id:
            flag = True
    if flag == False:
        return jsonify({'error':'RoomNotFound'})
    return jsonify({'nbMeasures':db.select_nbr_measures_room(room_id)})

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
{
"humidity": 20.0,
"luminance": 130.4,
"room": "A432",
"temperature": 27.4
}

@apiError RoomNotFound The <code>id</code> of the Room was not found.
@apiError TooMuchMeasures The number of measures to take is bigger than the total of measures.

@apiErrorExample {json} Error-Response:
{
    "error": "RoomNotFound"
}
@apiErrorExample {json} Error-Response:
{
  "error": "TooMuchMeasures",
  "max": 234
}

"""
@app.route('/<string:room_id>/average/<int:x>', methods=['GET'])
def get_room_avg(room_id, x):
    flag = False
    rooms = db.select_all_rooms()
    for room in rooms:
        if room == room_id:
            flag = True
    if flag == False:
        return jsonify({'error':'RoomNotFound'})
    nbr = db.select_nbr_measures_room(room_id)
    if x > nbr:
        return jsonify({'error':'TooMuchMeasures', 'max':nbr})
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
@apiError ControllerNotFound The <code>name</code> of the Controller was not found.
@apiError SensorNotFound The <code>id</code> of the Sensor was not found.

@apiErrorExample {json} Error-Response:
{
	"error": "ControllerNotFound"
}
@apiErrorExample {json} Error-Response:
{
	"error": "SensorNotFound"
}
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
        return jsonify({'error':'ControllerNotFound'})

    # check if the sensor exists
    flag = False
    sensors = db.select_all_sensors(controller)
    for sens in sensors:
        if sens.get('id') == sensor:
            flag = True
    if flag == False:
        return jsonify({'error':'SensorNotFound'})

    return jsonify(db.select_measures_between(controller, sensor, date1, date2))

"""
@api {get} /v0/radiator/read/:id get Radiator value
@apiName GetRadiatorValue
@apiGroup Store-Radiator

@apiExample {curl} Example usage:
curl -i http://localhost:5000/v0/radiator/read/1

@apiParam {int} id Radiator id

@apiSuccess {str} current_value Radiator value

@apiSuccessExample {json} Success-Response:
{
"current_value": "20"
}

@apiError RadiatorNotFound The <code>id</code> of the Radiator was not found.

@apiErrorExample {json} Error-Response:
{
    "error": "RadiatorNotFound"
}
"""
@app.route('/v0/radiator/read/<int:id>', methods=['GET'])
def get_radiator_value(id):
    '''flag = False
    rooms = db.select_all_rooms()
    for room in rooms:
        if room == room_id:
            flag = True
    if flag == False:
        return jsonify({'error':'RoomNotFound'})
    nbr = db.select_nbr_measures_room(room_id)
    if x > nbr:
        return jsonify({'error':'TooMuchMeasures', 'max':nbr}) '''
    return jsonify({'error':'RadiatorNotFound'})

"""
@api {get} /v0/store/read/:id get Store value
@apiName GetStoreValue
@apiGroup Store-Radiator

@apiExample {curl} Example usage:
curl -i http://localhost:5000/v0/store/read/1

@apiParam {int} id Store id

@apiSuccess {str} current_value Store value

@apiSuccessExample {json} Success-Response:
{
"current_value": "20"
}

@apiError RadiatorNotFound The <code>id</code> of the Store was not found.

@apiErrorExample {json} Error-Response:
{
    "error": "StoreNotFound"
}
"""
@app.route('/v0/store/read/<int:id>', methods=['GET'])
def get_store_value(id):
    '''flag = False
    rooms = db.select_all_rooms()
    for room in rooms:
        if room == room_id:
            flag = True
    if flag == False:
        return jsonify({'error':'RoomNotFound'})
    nbr = db.select_nbr_measures_room(room_id)
    if x > nbr:
        return jsonify({'error':'TooMuchMeasures', 'max':nbr}) '''
    return jsonify({'error':'StoreNotFound'})

"""
@api {get} /v0/store/write/:id/:x set Store value
@apiName SetStoreValue
@apiGroup Store-Radiator

@apiExample {curl} Example usage:
curl -i http://localhost:5000/v0/store/write/1/42

@apiDescription Here we use a GET method to POST new
data on the REST server. It is easier to use and you can verify
the new data of the Store by checking the success response.

@apiParam {int} id Store id
@apiParam {int} x Store value

@apiSuccess {str} new_value Store value

@apiSuccessExample {json} Success-Response:
{
"new_value": "42"
}

@apiError StoreNotFound The <code>id</code> of the Store was not found.
@apiError WrongValue The <code>x</code> value is wrong.

@apiErrorExample {json} Error-Response:
{
    "error": "StoreNotFound"
}

@apiErrorExample {json} Error-Response:
{
    "error": "WrongValue",
    "min_value": "0",
    "max_value": "255"
}
"""
@app.route('/v0/store/write/<int:id>/<int:x>', methods=['GET'])
def set_store_value(id,x):
    requests.post('http://localhost:5001/v0/store/write',json={'store_id':str(id),'value' : str(x)})
    return jsonify({'new_value':str(x)})

"""
@api {get} /v0/radiator/write/:id/:x set Radiator value
@apiName SetRadiatorValue
@apiGroup Store-Radiator

@apiExample {curl} Example usage:
curl -i http://localhost:5000/v0/radiator/write/1/42

@apiDescription Here we use a GET method to POST new
data on the REST server. It is easier to use and you can verify
the new data of the Radiator by checking the success response.

@apiParam {int} id Radiator id
@apiParam {int} x Radiator value

@apiSuccess {str} new_value Radiator value

@apiSuccessExample {json} Success-Response:
{
"new_value": "42"
}

@apiError RadiatorNotFound The <code>id</code> of the Radiator was not found.
@apiError WrongValue The <code>x</code> value is wrong.

@apiErrorExample {json} Error-Response:
{
    "error": "RadiatorNotFound"
}

@apiErrorExample {json} Error-Response:
{
    "error": "WrongValue",
    "min_value": "0",
    "max_value": "255"
}
"""
@app.route('/v0/radiator/write/<int:id>/<int:x>', methods=['GET'])
def set_radiator_value(id,x):
    requests.post('http://localhost:5001/v0/radiator/write',json={'radiator_id':str(id),'value' : str(x)})
    return jsonify({'new_value':str(x)})

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
