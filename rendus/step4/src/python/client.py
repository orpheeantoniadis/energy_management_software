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

db = database()

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

def delete_all_rules(db):
	rules = db.select_all_rules()
	for rule in rules:
		db.delete_rule(rule)

def check_rules(db):
	rules = db.select_all_rules()
	for rule in rules:
		if rule.get_rule() == 1:
			check_rule_1(db,rule)
		elif rule.get_rule() == 2:
			check_rule_2(db,rule)
		elif rule.get_rule() == 3:
			check_rule_3(db,rule)
		elif rule.get_rule() == 4:
			check_rule_4(db,rule)

'''
Rule 1: lower the temperature of a room to a given threshold when it is empty.
As we know that we have 2 radiators in a room, we drive both.
'''
def check_rule_1(db,rule):
    datas = db.select_room_last(rule.get_location())
    if datas.get('motion') == False:
        if datas.get('temperature') > rule.get_threshold():
            radiators = db.select_drivers(rule.get_location(),'radiator')
            requests.post('http://localhost:5001/v0/radiator/write',
            json={'radiator_id':str(radiators[0].get_id()),'value' : '0'})
            requests.post('http://localhost:5001/v0/radiator/write',
            json={'radiator_id':str(radiators[1].get_id()),'value' : '0'})
            db.insert_driver(radiators[0].get_id(),'radiator',0,rule.get_location(),date=None)
            db.insert_driver(radiators[1].get_id(),'radiator',0,rule.get_location(),date=None)

'''
Rule 2: increase the temperature of a room to a given threshold when it is occupied.
As we know that we have 2 radiators in a room, we drive both.
'''
def check_rule_2(db,rule):
    datas = db.select_room_last(rule.get_location())
    if datas.get('motion') == True:
        if datas.get('temperature') < rule.get_threshold():
            radiators = db.select_drivers(rule.get_location(),'radiator')
            requests.post('http://localhost:5001/v0/radiator/write',
            json={'radiator_id':str(radiators[0].get_id()),'value' : '200'})
            requests.post('http://localhost:5001/v0/radiator/write',
            json={'radiator_id':str(radiators[1].get_id()),'value' : '200'})
            db.insert_driver(radiators[0].get_id(),'radiator',200,rule.get_location(),date=None)
            db.insert_driver(radiators[1].get_id(),'radiator',200,rule.get_location(),date=None)

'''
Rule 3: close the stores when the humidity is high.
As we know that we have 2 stores in a room, we drive both.
'''
def check_rule_3(db,rule):
    datas = db.select_room_last(rule.get_location())
    if datas.get('humidity') > rule.get_threshold():
        stores = db.select_drivers(rule.get_location(),'store')
        requests.post('http://localhost:5001/v0/store/write',
        json={'store_id':str(stores[0].get_id()),'value' : '0'})
        requests.post('http://localhost:5001/v0/store/write',
        json={'store_id':str(stores[1].get_id()),'value' : '0'})
        db.insert_driver(stores[0].get_id(),'store',0,rule.get_location(),date=None)
        db.insert_driver(stores[1].get_id(),'store',0,rule.get_location(),date=None)

'''
Rule 4: open the store at day time, when the luminance is low and the room is occupied.
Here we do not check if it is day time because it can change (not the same
in the summer and at december). We thing that luminance is more important, especially
when the room is occupied.
As we know that we have 2 stores in a room, we drive both.
'''
def check_rule_4(db,rule):
    datas = db.select_room_last(rule.get_location())
    if datas.get('motion') == True:
        if datas.get('luminance') < rule.get_threshold():
            stores = db.select_drivers(rule.get_location(),'store')
            requests.post('http://localhost:5001/v0/store/write',
            json={'store_id':str(stores[0].get_id()),'value' : '255'})
            requests.post('http://localhost:5001/v0/store/write',
            json={'store_id':str(stores[1].get_id()),'value' : '255'})
            db.insert_driver(stores[0].get_id(),'store',255,rule.get_location(),date=None)
            db.insert_driver(stores[1].get_id(),'store',255,rule.get_location(),date=None)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    pi_list = []
    pi_list.append(rasp(IP_RASP1, PORT))
    pi_list.append(rasp(IP_RASP2, PORT))
    pi_list.append(rasp(IP_RASP3, PORT))

    #db = database()
    for pi in pi_list:
        db.insert_pi(pi)
        for sensor in pi.sensors_list:
            db.insert_sensor(sensor)

    delete_all_rules(db)
    init_drivers(db)

    #to execute every ~4min
    while True:
        print "collecting data...\n"
        for pi in pi_list:
        	for sensor in pi.sensors_list:
        		db.insert_measures(sensor)
        check_rules(db)
        print "waiting...\n"
        time.sleep(240) #240
