#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rasp import *

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
	test = rasp1.get_sensor_datas(2)
	print rasp1.get_sensor_datas(2)
	print test.get('updateTime')
	print test.get('battery')
