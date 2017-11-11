#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2
from configparser import ConfigParser
import datetime
from rasp import *
from sensor import *

class database(object):
	def __init__(self):
		params = self.config()
		self.connection = psycopg2.connect(**params)
		self.cursor = self.connection.cursor()

	def config(self, filename='database.ini', section='postgresql'):
		parser = ConfigParser()
		parser.read(filename)
		db = {}
		if parser.has_section(section):
			params = parser.items(section)
			for param in params:
				db[param[0]] = param[1]
		else:
			raise Exception('Section {0} not found in the {1} file'.format(section, filename))
		
		return db

	def select_all_measures(self):
		self.cursor.execute("SELECT * FROM mesures")
		measures = []
		row = self.cursor.fetchone()
		while row is not None:
			measures.append({'id':row[0], 'controller':row[1], 'humidity':row[2], 'luminance':row[3], 'temperature':row[4], 'battery': row[5], 'date':row[6], 'motion':row[7]})
			row = self.cursor.fetchone()
		return measures
	
	def select_last_measure(self, pi, sensor):
		sql = "SELECT * FROM mesures WHERE controller ILIKE 'Pi %s' AND id = %s ORDER BY date DESC"
		self.cursor.execute(sql, (pi, sensor))
		row = self.cursor.fetchone()
		measure = {'humidity':row[2], 'luminance':row[3], 'temperature':row[4],\
		'battery': row[5], 'date':row[6], 'motion':row[7]}
		return measure
	
	def select_room_avg(self, room, x):
		sql = "SELECT location, AVG(humidity), AVG(luminence), AVG(temperature) " +\
		"FROM (SELECT s.location, m.humidity, m.luminence, m.temperature "+\
		"FROM mesures m JOIN sensors s ON m.id = s.id "+\
		"WHERE s.location ILIKE %s ORDER BY date DESC LIMIT %s) l GROUP BY location"
		self.cursor.execute(sql, (room, x))
		row = self.cursor.fetchone()
		measure = {'room':row[0], 'humidity':float(row[1]), 'luminance':float(row[2]),\
		'temperature':float(row[3])}
		return measure
	
	def select_measures_between(self, pi, sensor, date1, date2):
		sql = "SELECT * FROM mesures WHERE controller ILIKE 'Pi %s' AND id = %s AND date BETWEEN %s AND %s"
		self.cursor.execute(sql, (pi, sensor, date1, date2))
		measures = []
		row = self.cursor.fetchone()
		while row is not None:
			measures.append({'id':row[0], 'controller':row[1], 'humidity':row[2], 'luminance':row[3], 'temperature':row[4], 'battery': row[5], 'date':row[6], 'motion':row[7]})
			row = self.cursor.fetchone()
		return measures

	def insert_pi(self, pi):
		# checks if the pi already exists in the database
		self.cursor.execute("SELECT * FROM pi")
		row = self.cursor.fetchone()
		while row is not None:
			if pi.ip == row[0]:
				return
			row = self.cursor.fetchone()

		sql = "INSERT INTO pi VALUES(%s, %s, %s);"
		self.cursor.execute(sql, (pi.ip, pi.port, pi.sensors_list[0].controller))
		self.connection.commit()

	def insert_sensor(self, sensor):
		# checks if the sensor already exists in the database
		self.cursor.execute("SELECT * FROM sensors")
		row = self.cursor.fetchone()
		while row is not None:
			if int(sensor.id) == row[0] and sensor.controller == row[1]:
				return
			row = self.cursor.fetchone()

		sql = "INSERT INTO sensors VALUES(%s, %s, %s);"
		self.cursor.execute(sql, (sensor.id, sensor.controller, sensor.location))
		self.connection.commit()

	def insert_measures(self, sensor):
		# converts timestamp into readable string
		date = datetime.datetime.fromtimestamp(\
		sensor.get_measure('updateTime')).strftime('%Y-%m-%d %H:%M:%S')

		# checks if the data already exists in the database
		sql = "SELECT * FROM mesures WHERE id = %s and controller ILIKE %s"
		self.cursor.execute(sql, (sensor.id, sensor.controller))
		row = self.cursor.fetchone()
		while row is not None:
			if date == str(row[6]):
				return
			row = self.cursor.fetchone()

		sql = "INSERT INTO mesures VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
		self.cursor.execute(sql, (sensor.id, sensor.controller,\
		sensor.get_measure('humidity'), sensor.get_measure('luminance'),\
		sensor.get_measure('temperature'), sensor.get_measure('battery'),\
		date, sensor.get_measure('motion')))
		self.connection.commit()

	def close(self):
		self.cursor.close()
		self.connection.close()
