#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2
from configparser import ConfigParser

class Database(object):

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

    def insert_measures(self,id, controller, humid, lum, temp, bat, date, motion):
        self.cursor.execute("INSERT INTO mesures VALUES(" + str(id) + ',' + controller + ',' + str(humid) + ',' + str(lum) + ',' + str(
                temp) + ',' + str(bat) + ',' + date + ',' + motion + ")")

    def close(self):
        self.cursor.close()
        self.connection.close()
