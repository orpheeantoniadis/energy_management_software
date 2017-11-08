#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2
import datetime
from rasp import *
from sensor import *

class database(object):
	def __init__(self, dbname, user, password=None):
		self.dbname = dbname
		self.user = user
		self.db = "dbname=" + self.dbname + " user=" + self.user + " password="
		if password is not None:
			self.connection = psycopg2.connect("dbname=" + self.dbname + " user=" + self.user + " password=")
			self.db = self.db + password

		self.connection = psycopg2.connect(self.db)
		self.cursor = self.connection.cursor()

	def select_all_measures(self):
		self.cursor.execute("SELECT * FROM mesures")
		measures = []
		row = self.cursor.fetchone()
		while row is not None:
			measures.append({'id':row[0], 'controller':row[1], 'humidity':row[2], 'luminence':row[3], 'temperature':row[4], 'battery': row[5], 'date':row[6], 'motion':row[7]})
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
