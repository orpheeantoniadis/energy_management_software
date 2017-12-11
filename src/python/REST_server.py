#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import *
from database import *
from configparser import ConfigParser
import requests
from rule import *

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
    value = db.select_driver_value(id,'radiator')
    if value == None:
        return jsonify({'error':'RadiatorNotFound'})
    return jsonify({'current_value':str(value)})

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
    value = db.select_driver_value(id,'store')
    if value == None:
        return jsonify({'error':'StoreNotFound'})
    return jsonify({'current_value':str(value)})

"""
@api {post} /rules set Rules
@apiName SetRules
@apiGroup Store-Radiator

@apiDescription Here we POST a json with a new rule / fonctionnality. 4 rules
are available:

1. Lower the temperature of a room to a given threshold when it is empty
2. Increase the temperature of a room to a given threshold when it is occupied
3. Close the stores when the humidity is high
4. Open the store at day time, when the luminance is low and the room is occupied

@apiParam {int} rule Rule number
@apiParam {string} location The room in which the rule is applied
@apiParam {int} thresholed The value the rule is triggered on. For <code>rules 1 & 2</code>,
the thresholed is a temperature <code>[0..30]</code> (°C), for <code>rule 3</code> this is
a humidity value <code>[0..100]</code> (%) and finnaly for <code>rule 4</code>, the threshold is a limunance
value <code>[0..1000]</code> (Candela).

@apiSuccess {str} ok ok

@apiParamExample {json} Exemple-JSON:
{
    "rule": 1,
    "location": "A532",
    "threshold": 20,
}
@apiParamExample {json} Exemple-JSON:
{
    "rule": 4,
    "location": "A401",
    "threshold": 100,
}

@apiSuccessExample {json} Success-Response:
{
    "ok": "ok"
}

@apiError WrongRuleNBR The <code>nbr</code> of the Rule was not found.
@apiError WrongThreshold The <code>threshold</code> value is wrong.
@apiError WrongLocation The <code>location</code> doesn't exist.

@apiErrorExample {json} Error-Response:
{
    "error": "WrongRuleNBR"
}

@apiErrorExample {json} Error-Response:
{
    "error": "WrongLocation"
}

@apiErrorExample {json} Error-Response:
{
    "error": "WrongThreshold",
    "min_value": "0",
    "max_value_temp": "30",
    "max_value_lum": "1000",
    "max_value_hum": "100"
}
"""
@app.route('/rules', methods=['POST'])
def set_rules():
    datas = request.get_json()
    rule = datas.get('rule')
    if (rule < 0) or (rule > 5):
        return jsonify({'error':'WrongRuleNBR'})
    location = datas.get('location')
    flag = False
    for room in db.select_all_rooms():
        if location == room:
            flag = True
    if flag == False:
        return jsonify({'error':'WrongLocation'})
    threshold = datas.get('threshold')
    thError = jsonify({'error':'WrongThreshold','min_value':'0',
        'max_value_temp':'30','max_value_lum':'1000','max_value_hum':'100'})
    if (rule == 1) or (rule == 2):
        if (threshold<0)or(threshold>30):
            return thError
    elif rule == 3:
        if (threshold<0)or(threshold>100):
            return thError
    else:
        if (threshold<0)or(threshold>1000):
            return thError
    #db.insert_rule(datas.get('rule'),datas.get('location'),datas.get('threshold'))
    return jsonify({'ok':'ok'})


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
