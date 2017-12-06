#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import *
import requests
from configparser import ConfigParser

SERVER_PORT=5001 # REST sserver of the professor

app = Flask(__name__)


def set_radiator(id,value):
    requests.post('http://localhost:5001/v0/radiator/write',json={'radiator_id':str(id),'value' : str(value)})

def set_store(id,value):
    requests.post('http://localhost:5001/v0/store/write',json={'store_id':str(id),'value' : str(value)})


if __name__ == '__main__':
    set_radiator(1,100)
    set_store(1,150)
        #app.run(debug=True,host=ip[1])
