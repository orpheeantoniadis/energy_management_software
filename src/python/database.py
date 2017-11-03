#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2

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

	def insert_pi(self, ip, port, name):
		self.cursor.execute("SELECT * FROM pi")
		row = self.cursor.fetchone()
		while row is not None:
			if ip == row[0]:
				return
			row = self.cursor.fetchone()
		sql = "INSERT INTO pi VALUES(%s, %s, %s);"
		self.cursor.execute(sql, (ip, port, name))
		self.connection.commit()

	def insert_sensor(self, id, controller, location):
		self.cursor.execute("SELECT * FROM sensors")
		row = self.cursor.fetchone()
		while row is not None:
			if int(id) == row[0] and controller == row[1]:
				return
			row = self.cursor.fetchone()
		sql = "INSERT INTO sensors VALUES(%s, %s, %s);"
		self.cursor.execute(sql, (id, controller, location))
		self.connection.commit()

	def insert_measures(id, controller, humid, lum, temp, bat, date, motion):
		conn = psycopg2.connect("dbname=distributed user=postgres password=")
		cur = conn.cursor()
		cur.execute("INSERT INTO mesures VALUES("+str(id)+" "+controller+" "+str(humid)+" "+str(lum)+" "+str(temp)+" "+str(bat)+" "+date+" "+str(motion)+")")
		cur.execute("INSERT INTO mesures VALUES(3,'Pi lab1',22,null,12,100,'2010-10-19 10:35:54',false)")

	def close(self):
		self.cursor.close()
		self.connection.close()
