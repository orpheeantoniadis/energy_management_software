#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib
import json

class driver(object):
	def __init__(self, id, type, value, location, last_modif):
		self.id = id
		self.type = type
		self.value = value
		self.location = location
		self.last_modif = last_modif

	def get_id(self):
		return self.id

	def get_type(self):
		return self.type

	def get_value(self):
		return self.value

	def get_location(self):
		return self.location

	def get_last_modif(self):
		return self.last_modif

	def __str__(self):
		return str(str(self.id) + self.type + str(self.value) + self.location + str(self.last_modif))
