#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import time
import signal
from rasp import *
from database import *

IP_RASP1 = "129.194.184.124"
IP_RASP2 = "129.194.184.125"
IP_RASP3 = "129.194.185.199"
PORT = "5000"

def signal_handler(signal, frame):
	db.close()
	sys.exit(0)

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

	# to execute every ~4min
	while True:
		print "collecting data...\n"
		for pi in pi_list:
			for sensor in pi.sensors_list:
				db.insert_measures(sensor)
		print "waiting...\n"
		time.sleep(240)