#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import time
import signal
from rasp import *
from database import *
import requests

IP_RASP1 = "129.194.184.124"
IP_RASP2 = "129.194.184.125"
IP_RASP3 = "129.194.185.199"
PORT = "5000"

'''
This function init the drivers into the database by reading the drivers.ini file AND
set the drivers values. (drivers = radiators/stores)
'''
def init_drivers(db):
    parser = ConfigParser()
    parser.read('drivers.ini')
    sections = parser.sections()
    for driver in sections:
        params = parser.items(driver)
        id = params[0][1]
        type = params[1][1]
        value = params[2][1]
        location = params[3][1]
        requests.post('http://localhost:5001/v0/'+type+'/write',json={type+'_id':str(id),'value' : str(value)})
        db.insert_driver(id,type,value,location,date=None)

def signal_handler(signal, frame):
	db.close()
	sys.exit(0)

def check_rules(db):
	rules = db.select_all_rules()
	for rule in rules:
		print(rool)
		check_rule(db,rule)

def check_rule(db,rool):
	threshold = rule.get_threshold()
	room = rule.get_location()
	if rule.get_rule() == 1:

	elif: rule.get_rule() == 2:

	elif: rule.get_rule() == 3:

	elif: rule.get_rule() == 4:

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)

	pi_list = []
	pi_list.append(rasp(IP_RASP1, PORT))
	pi_list.append(rasp(IP_RASP2, PORT))
	pi_list.append(rasp(IP_RASP3, PORT))

	db = database()
	for pi in pi_list:
		db.insert_pi(pi)
		for sensor in pi.sensors_list:
			db.insert_sensor(sensor)

	#init_drivers(db)
	check_rules(db)
	# to execute every ~4min
	# while True:
	# 	print "collecting data...\n"
	# 	for pi in pi_list:
	# 		for sensor in pi.sensors_list:
	# 			db.insert_measures(sensor)
	# 	print "waiting...\n"
	# 	time.sleep(240)
