#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psycopg2
from configparser import ConfigParser

if __name__ == '__main__':
	conn = psycopg2.connect("dbname=exo3 user=Orphee password=")
	cur = conn.cursor()
	cur.execute("SELECT * FROM auteurs")
	row = cur.fetchone()
	while row is not None:
	    print(row)
	    row = cur.fetchone()

	cur.close()
	conn.close()
