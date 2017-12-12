var async = require('async');
var Client = require('node-rest-client').Client;

var controllers = [];
var sensors = [];
var controllerSel;
var sensorSel;

console.log('Program Start');

async.series([
  function (callback) {
		console.log('First Step --> ');
		var client = new Client();
		client.registerMethod("jsonMethod", "http://localhost:5000/controllers_list", "GET");
		client.methods.jsonMethod(function (data, response) {
			controllers = Array.from(data);
			controllerSel = controllers[0].name;
			callback(null, data);
		});
  },
  function (callback) {
    console.log('Second Step --> ');
		var client = new Client();
		client.registerMethod("jsonMethod", "http://localhost:5000/"+controllerSel+"/sensors_list", "GET");
		client.methods.jsonMethod(function (data, response) {
			sensors = Array.from(data);
			sensorSel = sensors[0].id;
			callback(null, data);
		});
  },
	function (callback) {
    console.log('Third Step --> ');
		var client = new Client();
		client.registerMethod("jsonMethod", "http://localhost:5000/"+controllerSel+"/"+sensorSel+"/last_measures", "GET");
		client.methods.jsonMethod(function (data, response) {
			callback(null, data);
		});
  }
],
function (err, result) {
    console.log(result);
});

console.log('Program End');