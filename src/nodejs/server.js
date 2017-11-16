var express = require('express');
var session = require('express-session');
var parseurl = require('parseurl')
var bodyParser = require('body-parser');
var Client = require('node-rest-client').Client;

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });

var controllers = [];
var sensors = [];
var controllerSel;
var sensorSel;

app.use(session({
  secret: 'secretkey',
  resave: false,
  saveUninitialized: true
}))

.use(express.static(__dirname + "/node_modules"))

.use(express.static(__dirname + "/views"))

.use(express.static(__dirname + '/../apidoc'))

// initialisation des variables de la session
.use(function(req, res, next) {
	if (typeof(req.session.controllers) == 'undefined') {
		req.session.controllers = [];
	} else if (req.session.controllers.length == 0) {
		req.session.controllers = controllers;
		req.session.controllerSel = controllerSel;
	} else if (typeof(req.session.sensors) == 'undefined') {
		req.session.sensors = [];
	} else if (req.session.sensors.length == 0) {
		req.session.sensors = sensors;
		req.session.sensorSel = sensorSel;
	} else if (typeof(req.session.datarangeMode) == 'undefined') {
		req.session.datarangeMode = false;
	} else if (typeof(req.session.datarange) == 'undefined') {
		req.session.datarange = [];
	}
	next();
})

.use(function(req, res, next) {
	if (controllers.length == 0) {
		var client = new Client();
		client.registerMethod("jsonMethod", "http://localhost:5000/controllers_list", "GET");
		client.methods.jsonMethod(function (data, response) {
			controllers = Array.from(data);
			controllerSel = controllers[0].name;
			var client = new Client();
			client.registerMethod("jsonMethod", "http://localhost:5000/"+controllers[0].name+"/sensors_list", "GET");
			client.methods.jsonMethod(function (data, response) {
				sensors = Array.from(data);
				sensorSel = sensors[0].id;
			});
		});
	}
	next();
})

.get('/', function(req, res) {
	res.render('pages/index.ejs', {url : parseurl(req).pathname});
})

.get('/sensors', function(req, res) {
	var client = new Client();
	if (!req.session.datarangeMode) {
		client.registerMethod("jsonMethod", "http://localhost:5000/"+req.session.controllerSel+
		"/"+req.session.sensorSel+"/last_measures", "GET");
		client.methods.jsonMethod(function (data, response) {
			res.render('pages/sensors.ejs', {
				url:  parseurl(req).pathname,
				controllers: req.session.controllers,
				sensors: req.session.sensors,
				controllerSel: req.session.controllerSel,
				sensorSel: req.session.sensorSel,
				measures: data
			});
		});
	} else {
		client.registerMethod("jsonMethod", "http://localhost:5000/"+req.session.controllerSel+
		"/"+req.session.sensorSel+"/"+req.session.datarange[0]+"/"+req.session.datarange[1], "GET");
		client.methods.jsonMethod(function (data, response) {
			res.render('pages/sensors.ejs', {
				url:  parseurl(req).pathname, 
				controllers: req.session.controllers,
				sensors: req.session.sensors,
				controllerSel: req.session.controllerSel,
				sensorSel: req.session.sensorSel,
				measures: data
			});
		});
	}
})

.post('/sensors/selection', urlencodedParser, function(req, res) {
	req.session.datarangeMode = false;
	if (req.session.controllerSel != req.body.controller) {
		var client = new Client();
		req.session.controllerSel = req.body.controller;
		client.registerMethod("jsonMethod", "http://localhost:5000/"+req.session.controllerSel+
		"/sensors_list", "GET");
		client.methods.jsonMethod(function (data, response) {
			req.session.sensors = Array.from(data);
			req.session.sensorSel = req.session.sensors[0].id;
			res.redirect('/sensors');
		});
	} else {
		req.session.controllerSel = req.body.controller;
		req.session.sensorSel = req.body.sensor;
		res.redirect('/sensors');
	}
})

.post('/sensors/daterange', urlencodedParser, function(req, res) {
	req.session.datarangeMode = true;
	req.session.datarange = req.body.daterange.split(' - ');
	res.redirect('/sensors');
})

.get('/rooms', function(req, res) {
	res.render('pages/rooms.ejs', {url : parseurl(req).pathname});
})

.get('/test', function(req, res) {
	res.render('pages/test.ejs', {url : parseurl(req).pathname});
})

.listen(8080);