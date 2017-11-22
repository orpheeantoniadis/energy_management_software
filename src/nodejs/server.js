var express = require('express');
var session = require('express-session');
var parseurl = require('parseurl');
var bodyParser = require('body-parser');
var Client = require('node-rest-client').Client;

var tools = require('./rest-tools');

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });

app.use(session({
  secret: 'secretkey',
  resave: false,
  saveUninitialized: true
}))

.use(express.static(__dirname + "/node_modules"))

.use(express.static(__dirname + "/views"))

.use(express.static(__dirname + '/../apidoc'))

.get('/', function(req, res) {
	res.render('pages/index.ejs', {url : parseurl(req).pathname});
})

.get('/sensors', function(req, res) {
	var client = new Client();
	if (!req.session.datarangeMode) {
		tools.getLastMeasures(req, res);
	} else {
		tools.getMeasuresBetween(req, res);
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