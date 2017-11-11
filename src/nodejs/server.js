var express = require('express');
var session = require('cookie-session');
var Client = require('node-rest-client').Client;
var path = require("path");

var app = express();
var client = new Client();
 
// registering remote methods 
// client.registerMethod("jsonMethod", "http://localhost:5000/1/4/last_measures", "GET");
client.registerMethod("jsonMethod", "http://localhost:5000/controllers_list", "GET");

 
client.methods.jsonMethod(function (data, response) {
    console.log(data);
		console.log(Array.from(data));
		console.log(data[1]);
});

app.use(session({ secret: 'secretodolist' }))

.use(express.static(__dirname + "/node_modules"))

.use(express.static(__dirname + "/views/css"))

.use(express.static(__dirname + '/../apidoc'))

.use(function(req, res, next) {
	if (typeof(req.session.controllers) == 'undefined') {
		req.session.controllers = [];
	}
	next();
})

.get('/', function(req, res) {
	res.render('pages/index.ejs', {query : '/'});
})

.get('/sensors', function(req, res) {
	var controllers = [];
	client.registerMethod("jsonMethod", "http://localhost:5000/controllers_list", "GET");
	client.methods.jsonMethod(
		function (data, response) {
			controllers.push(Array.from(data));
			return data;
		}
	);
	console.log(controllers);
	res.render('pages/sensors.ejs', { query: '/sensors', controllers: req.session.controllers });
})

.listen(8080);