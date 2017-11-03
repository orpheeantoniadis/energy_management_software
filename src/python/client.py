#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rasp import *
from database import *

IP_RASP1 = "129.194.184.124"
IP_RASP2 = "129.194.184.125"
IP_RASP3 = "129.194.185.199"
PORT = "5000"

if __name__ == '__main__':
	rasp1 = rasp(IP_RASP1, PORT)
	rasp2 = rasp(IP_RASP2, PORT)
	rasp3 = rasp(IP_RASP3, PORT)
	print(rasp1)
	print(rasp2)
	print(rasp3)
	print rasp1.sensors_list[5].get_measure('temperature')
	print rasp1.sensors_list[5].get_measure('updateTime')
	print rasp1.sensors_list[5].get_measure('battery')

	db = Database("distributed","postgres")
    measures = db.select_all_measures()
	print measures
    print measures[0]
    print measures[2]
    print measures[0]['id']
    print measures[0]['controller']
    print measures[0]['humidity']
    print measures[0]['motion']
    db.close()
