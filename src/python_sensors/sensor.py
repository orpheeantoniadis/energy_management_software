#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib
import json

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

	def get_all_measures(self):
		url = "http://" + self.ip + ":" + self.port + "/sensors/" + self.id + "/get_all_measures"
		response = urllib.urlopen(url)
		measures = json.loads(response.read())
		return measures

	def get_measure(self, data):
		measures = self.get_all_measures()
		return measures.get(data)

	def __str__(self):
		return str(self.id)
