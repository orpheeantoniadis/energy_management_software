#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib, json

url = "http://129.194.184.124:5000/sensors/4/get_all_measures"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data
