#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib, json
from sensor import *

class rasp(object):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sensors_list = self.get_sensors_list()

	def get_sensors_list(self):
		sensors_list = []
		url = "http://" + self.ip + ":" + self.port + "/sensors/get_sensors_list"
		response = urllib.urlopen(url)
		sensors_id_list =  json.loads(response.read()).keys()
		for sensor_id in sensors_id_list :
			sensors_list.append(sensor(self.ip, self.port, sensor_id))
		return sensors_list

	def __str__(self):
		temp = str(self.ip) + "\n" +\
		str(self.port) + "\n" + "{ "
		for sensor in self.sensors_list :
			temp += str(sensor) + " "
		temp += "}\n"
		return temp
