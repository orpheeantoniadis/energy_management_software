#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2
from configparser import ConfigParser
import datetime
import time
from rasp import *
from sensor import *
from rule import *
from driver import *


class database(object):
	def __init__(self):
		params = self.config()
		self.connection = psycopg2.connect(**params)
		self.cursor = self.connection.cursor()
		self.rules = ["","Lower the temperature of a room to a given threshold when it is empty",
		        		"Increase the temperature of a room to a given threshold when it is occupied",
		        		"Close the stores when the humidity is high",
		        		"Open the store at day time, when the luminance is low and the room is occupied"]

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
		self.cursor.execute("SELECT * FROM measures")
		measures = []
		row = self.cursor.fetchone()
		while row is not None:
			measures.append({'id':row[0], 'controller':row[1], 'humidity':row[2], 'luminance':row[3], 'temperature':row[4], 'battery': row[5], 'date':row[6], 'motion':row[7]})
			row = self.cursor.fetchone()
		return measures

	def select_all_controllers(self):
		self.cursor.execute("SELECT * FROM pi")
		controllers = []
		row = self.cursor.fetchone()
		while row is not None:
			controllers.append({'ip':row[0], 'port':row[1], 'name':row[2]})
			row = self.cursor.fetchone()
		return controllers

	def select_all_sensors(self, pi):
		sql = "SELECT * FROM sensors WHERE controller ILIKE %s ORDER BY id ASC"
		self.cursor.execute(sql, (pi,))
		sensors = []
		row = self.cursor.fetchone()
		while row is not None:
			sensors.append({'id':row[0], 'controller':row[1], 'location':row[2]})
			row = self.cursor.fetchone()
		return sensors

	def select_last_measures(self, pi, sensor):
		sql = "SELECT * FROM measures WHERE controller ILIKE %s AND id = %s ORDER BY date DESC"
		self.cursor.execute(sql, (pi, sensor))
		row = self.cursor.fetchone()
		measures = [{'id':row[0], 'controller':row[1], 'humidity':row[2], 'luminance':row[3],\
		'temperature':row[4], 'battery': row[5], 'date':row[6], 'motion':row[7]}]
		return measures

	def select_room_avg(self, room, x):
		sql = "SELECT location, AVG(humidity), AVG(luminance), AVG(temperature) " +\
		"FROM (SELECT s.location, m.humidity, m.luminance, m.temperature "+\
		"FROM measures m JOIN sensors s ON m.id = s.id "+\
		"WHERE s.location ILIKE %s ORDER BY date DESC LIMIT %s) l GROUP BY location"
		self.cursor.execute(sql, (room, x))
		row = self.cursor.fetchone()
		measures = {'room':row[0], 'humidity':float(row[1]), 'luminance':float(row[2]),\
		'temperature':float(row[3])}
		return measures

	def select_room_last(self, room):
		sql = "SELECT * FROM measures m JOIN sensors s ON "+\
		"(m.id = s.id AND m.controller = s.controller) "+\
		"WHERE location ILIKE '"+room+"' ORDER BY date DESC LIMIT 1"
		self.cursor.execute(sql)
		row = self.cursor.fetchone()
		measures = {'room':row[10], 'humidity':float(row[2]), 'luminance':float(row[3]),\
		'temperature':float(row[4]),'motion':row[7]}
		return measures

	def select_nbr_measures_room(self,room):
		sql = "SELECT count(*) FROM sensors JOIN measures ON sensors.id = "+\
		"measures.id where location like '" + room + "'"
		self.cursor.execute(sql)
		row = self.cursor.fetchone()
		return row[0]

	def select_all_rooms(self):
		sql = "SELECT location FROM sensors GROUP BY location ORDER BY location ASC"
		self.cursor.execute(sql)
		rooms = []
		row = self.cursor.fetchone()
		while row is not None:
			rooms.append(row[0])
			row = self.cursor.fetchone()
		return rooms

	def select_measures_between(self, pi, sensor, date1, date2):
		sql = "SELECT * FROM measures WHERE controller ILIKE %s AND id = %s AND date BETWEEN %s AND %s"
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
		sql = "SELECT * FROM measures WHERE id = %s and controller ILIKE %s"
		self.cursor.execute(sql, (sensor.id, sensor.controller))
		row = self.cursor.fetchone()
		while row is not None:
			if date == str(row[6]):
				return
			row = self.cursor.fetchone()

		sql = "INSERT INTO measures VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
		self.cursor.execute(sql, (sensor.id, sensor.controller,\
		sensor.get_measure('humidity'), sensor.get_measure('luminance'),\
		sensor.get_measure('temperature'), sensor.get_measure('battery'),\
		date, sensor.get_measure('motion')))
		self.connection.commit()

	def close(self):
		self.cursor.close()
		self.connection.close()

	def insert_driver(self,id,type,value,location,date=None):
		if date is None:
			date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

		# check if the data already exists in database
		sql1 = "SELECT * FROM drivers WHERE id = %s AND type ILIKE %s"
		self.cursor.execute(sql1, (id, type))
		row = self.cursor.fetchone()
		self.connection.commit()
		# update DB
		if row is not None:
			sql = "UPDATE drivers set value=%s, last_modif=%s, location=%s WHERE id=%s AND type=%s"
			self.cursor.execute(sql,(str(value),date,str(location),str(id),type))
		else: # insert into db
			sql = "INSERT INTO drivers values(%s,%s,%s,%s,%s)"
			self.cursor.execute(sql,(str(id),type,str(value),str(location),date))

		self.connection.commit()

	def select_all_drivers(self):
		sql = "SELECT * FROM drivers"
		self.cursor.execute(sql)
		drivers = []
		row = self.cursor.fetchone()
		while row is not None:
			drivers.append(driver(row[0],row[1],row[2],row[3],row[4]))
			row = self.cursor.fetchone()
		return drivers

	def select_drivers(self,room,type):
		sql = "SELECT * FROM drivers WHERE location ILIKE %s AND type ILIKE %s"
		self.cursor.execute(sql,(room,type))
		drivers = []
		row = self.cursor.fetchone()
		while row is not None:
			drivers.append(driver(row[0],row[1],row[2],row[3],row[4]))
			row = self.cursor.fetchone()
		return drivers

	def select_driver_value(self,id,type):
		sql = "SELECT * FROM drivers WHERE id = %s AND type ILIKE %s"
		self.cursor.execute(sql, (id, type))
		row = self.cursor.fetchone()
		if row is not None:
			self.connection.commit()
			return row[2]
		self.connection.commit()
		return None

	def select_driver_date(self,id,type):
		sql = "SELECT * FROM drivers WHERE id = %s AND type ILIKE %s"
		self.cursor.execute(sql, (id, type))
		row = self.cursor.fetchone()
		if row is not None:
			self.connection.commit()
			return row[4]
		self.connection.commit()
		return None

	def select_driver_location(self,id,type):
		sql = "SELECT * FROM drivers WHERE id = %s AND type ILIKE %s"
		self.cursor.execute(sql, (id, type))
		row = self.cursor.fetchone()
		if row is not None:
			self.connection.commit()
			return row[3]
		self.connection.commit()
		return None

	def insert_rule(self,rule,location,threshold):
		# check if the data already exists in database
		sql1 = "SELECT * FROM rules WHERE rule = %s AND location ILIKE %s"
		self.cursor.execute(sql1, (rule, location))
		row = self.cursor.fetchone()
		self.connection.commit()
		# update DB
		if row is not None:
			sql = "UPDATE rules set threshold=%s, comment=%s WHERE rule=%s AND location ILIKE %s"
			self.cursor.execute(sql,(str(threshold),self.rules[rule],str(rule),str(location)))
		else: # insert into db
			sql = "INSERT INTO rules values(%s,%s,%s,%s)"
			self.cursor.execute(sql,(str(rule),str(location),str(threshold),self.rules[rule]))

		self.connection.commit()

	def select_all_rules(self):
		sql = "SELECT * FROM rules"
		self.cursor.execute(sql)
		rules = []
		row = self.cursor.fetchone()
		while row is not None:
			rules.append(rule(row[0],row[1],row[2]))
			row = self.cursor.fetchone()
		return rules

	def delete_rule(self,rule):
		sql = "DELETE FROM rules WHERE rule=%s AND location like %s"
		self.cursor.execute(sql,(rule.get_rule(),rule.get_location()))
		self.connection.commit()
