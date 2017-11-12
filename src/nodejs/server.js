var express = require('express');
var bodyParser = require('body-parser');
var Client = require('node-rest-client').Client;

var app = express();
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var client = new Client();

var controllers = [];
var sensors = [];

var controllerSel;
 
client.registerMethod("jsonMethod", "http://localhost:5000/controllers_list", "GET");

client.methods.jsonMethod(function (data, response) {
	controllers = Array.from(data);
});

app.use(express.static(__dirname + "/node_modules"))

.use(express.static(__dirname + "/views/css"))

.use(express.static(__dirname + '/../apidoc'))

.get('/', function(req, res) {
	res.render('pages/index.ejs', {url : '/'});
})

.get('/sensors', function(req, res) {
	res.render('pages/sensors.ejs', { url: '/sensors', controllers: controllers, 
	sensors: sensors,  controllerSel: controllerSel});
})

.post('/sensors/controller', urlencodedParser, function(req, res) {
	controllerSel = req.body.controller;
	client.registerMethod("jsonMethod", "http://localhost:5000/"+controllerSel+"/sensors_list", "GET");
	client.methods.jsonMethod(function (data, response) {
		sensors = Array.from(data);
	});
	res.redirect('/sensors');
})

.listen(8080);