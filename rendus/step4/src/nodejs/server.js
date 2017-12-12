var express = require('express');
var session = require('express-session');
var parseurl = require('parseurl');
var bodyParser = require('body-parser');
var fs = require('fs')
var ini = require('ini')
var tools = require('./rest-tools');

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var config = ini.parse(fs.readFileSync('../python/drivers.ini', 'utf-8'))

tools.setDrivers(config);

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
	if (!req.session.datarangeMode) {
		tools.getLastMeasures(req, res);
	} else {
		tools.getMeasuresBetween(req, res);
	}
})

.post('/sensors/selection', urlencodedParser, function(req, res) {
	req.session.datarangeMode = false;
	if (req.session.controllerSel != req.body.controller) {
		req.session.sensorSel = undefined;
	} else {
		req.session.sensorSel = req.body.sensor;
	}
	req.session.controllerSel = req.body.controller;
	res.redirect('/sensors');
})

.post('/sensors/daterange', urlencodedParser, function(req, res) {
	req.session.datarangeMode = true;
	req.session.datarange = req.body.daterange.split(' - ');
	res.redirect('/sensors');
})

.get('/rooms', function(req, res) {
	tools.getRadiatorsValues();
	tools.getStoresValues();
	tools.getRoomAvg(req, res);
})

.post('/rooms/selection', urlencodedParser, function(req, res) {
	req.session.nbMeasuresSel = undefined;
	req.session.roomSel = req.body.room;
	res.redirect('/rooms');
})

.post('/rooms/average', urlencodedParser, function(req, res) {
	req.session.nbMeasuresSel = req.body.nbMeasures;
	res.redirect('/rooms');
})

.post('/rooms/monitoring', urlencodedParser, function(req, res) {
	tools.postDriversThresholds(req);
	res.redirect('/rooms');
})

.get('/test', function(req, res) {
	res.render('pages/test.ejs', {url : parseurl(req).pathname});
})

.listen(8080);