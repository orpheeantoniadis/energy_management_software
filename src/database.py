#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2
from configparser import ConfigParser

if __name__ == '__main__':
	#conn = psycopg2.connect("dbname=exo3 user=Orphee password=")  ------- j'ai modifié ça petit Orphée
	conn = psycopg2.connect("dbname=distributed user=postgres password=")
	cur = conn.cursor()
	cur.execute("SELECT * FROM mesures")
	row = cur.fetchone()
	while row is not None:
	    print(row)
	    row = cur.fetchone()

	cur.close()
	conn.close()

	insert_mesures(3,"Pi lab1")


def insert_mesures(id,controller,humid,lum,temp,bat,date,motion):
	conn = psycopg2.connect("dbname=distributed user=postgres password=")
	cur = conn.cursor()
	cur.execute("INSERT INTO mesures VALUES("+str(id)+" "+controller+" "+str(humid)+" "+str(lum)+" "+str(temp)+" "+str(bat)+" "+date+" "+str(motion)+")")
	cur.close()
	conn.close()
	#cur.execute("INSERT INTO mesures VALUES(3,'Pi lab1',22,null,12,100,'2010-10-19 10:35:54',false)")
