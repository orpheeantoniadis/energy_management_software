#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib, json

class sensor(object):
	def __init__(self, ip, port, id):
		self.ip = ip
		self.port = port
		self.id = id
		url = "http://" + self.ip + ":" + self.port + "/sensors/" + self.id + "/get_all_measures"
		response = urllib.urlopen(url)
		measures = json.loads(response.read())
		self.controller = measures['controller']
		self.location = measures['location']
		self.updateTime = measures['updateTime']
		self.temperature = []
		self.humidity = []
		self.luminance = []
		self.motion = []
		self.update_measures()


	def update_measures(self):
		if self.updateTime != 'None':
			url = "http://" + self.ip + ":" + self.port + "/sensors/" + self.id + "/get_all_measures"
			response = urllib.urlopen(url)
			measures = json.loads(response.read())
			self.temperature.append(measures['temperature'])
			self.humidity.append(measures['humidity'])
			self.luminance.append(measures['luminance'])
			self.motion.append(measures['motion'])


	def __str__(self):
		return str(self.id)
