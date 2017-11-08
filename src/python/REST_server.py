#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from database import *

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/get_all_measures', methods=['GET'])
def get_tasks():
    return jsonify({'all_measures': db.select_all_measures()})

if __name__ == '__main__':
	db = database()
	app.run(debug=True)