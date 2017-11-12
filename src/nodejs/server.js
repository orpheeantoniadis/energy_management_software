var express = require('express');
var bodyParser = require('body-parser');
var Client = require('node-rest-client').Client;

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });

var controllers = [];
var sensors = [];

var controllerSel;
var sensorSel;

app.use(express.static(__dirname + "/node_modules"))

.use(express.static(__dirname + "/views/css"))

.use(express.static(__dirname + '/../apidoc'))

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
	res.render('pages/index.ejs', {url : '/'});
})

.get('/sensors', function(req, res) {
	var client = new Client();
	client.registerMethod("jsonMethod", "http://localhost:5000/"+controllerSel+"/"+sensorSel+"/last_measures", "GET");
	client.methods.jsonMethod(function (data, response) {
		res.render('pages/sensors.ejs', { url: '/sensors', controllers: controllers, 
		sensors: sensors,  controllerSel: controllerSel, sensorSel: sensorSel, measures: data});
	});
})

.post('/sensors/selection', urlencodedParser, function(req, res) {
	if (controllerSel != req.body.controller) {
		var client = new Client();
		controllerSel = req.body.controller;
		client.registerMethod("jsonMethod", "http://localhost:5000/"+controllerSel+"/sensors_list", "GET");
		client.methods.jsonMethod(function (data, response) {
			sensors = Array.from(data);
			sensorSel = sensors[0].id;
		});
	} else {
		controllerSel = req.body.controller;
		sensorSel = req.body.sensor;
	}
	res.redirect('/sensors');
})

.get('/rooms', function(req, res) {
	res.render('pages/rooms.ejs', {url : '/rooms'});
})

.listen(8080);