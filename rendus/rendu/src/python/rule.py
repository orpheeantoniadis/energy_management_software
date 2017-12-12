#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib
import json

class rule(object):
	def __init__(self, num, location, threshold):
		self.num = num
		self.location = location
		self.threshold = threshold

	def get_rule(self):
		return self.num

	def get_location(self):
		return self.location

	def get_threshold(self):
		return self.threshold

	def __str__(self):
		return str(str(self.num) + self.location + str(self.threshold))
