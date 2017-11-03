#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rasp import *
from database import *

IP_RASP1 = "129.194.184.124"
IP_RASP2 = "129.194.184.125"
IP_RASP3 = "129.194.185.199"
PORT = "5000"

if __name__ == '__main__':
	pi_list = []
	pi_list.append(rasp(IP_RASP1, PORT))
	pi_list.append(rasp(IP_RASP2, PORT))
	pi_list.append(rasp(IP_RASP3, PORT))
	for pi in pi_list:
		print pi

	db = database("sdi_ems","Orphee")
	for pi in pi_list:
		db.insert_pi(pi)
		for sensor in pi.sensors_list:
			db.insert_sensor(sensor)

	# to execute every ~4min
	for pi in pi_list:
		for sensor in pi.sensors_list:
			db.insert_measures(sensor)
	# measures = db.select_all_measures()
	# print measures
	db.close()
