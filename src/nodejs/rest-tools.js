var parseurl = require('parseurl');
var async = require('async');
var Client = require('node-rest-client').Client;

module.exports = {
  getLastMeasures: function (req, res) {
		async.series([
		  function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/controllers_list";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					req.session.controllers = Array.from(data);
					if (typeof(req.session.controllerSel) == 'undefined') {
						req.session.controllerSel = req.session.controllers[0].name;
					}
					callback(null, data);
				});
		  },
		  function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/"+req.session.controllerSel+"/sensors_list";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					req.session.sensors = Array.from(data);
					if (typeof(req.session.sensorSel) == 'undefined') {
						req.session.sensorSel = req.session.sensors[0].id;
					}
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/"+req.session.controllerSel+"/"+req.session.sensorSel+"/last_measures";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					callback(null, data);
				});
		  }
		],
		function (err, result) {
			res.render('pages/sensors.ejs', {
				url:  parseurl(req).pathname,
				controllers: req.session.controllers,
				sensors: req.session.sensors,
				controllerSel: req.session.controllerSel,
				sensorSel: req.session.sensorSel,
				measures: result[2]
			});
		});
  },
	
	getMeasuresBetween: function (req, res) {
		async.series([
		  function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/controllers_list";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					req.session.controllers = Array.from(data);
					if (typeof(req.session.controllerSel) == 'undefined') {
						req.session.controllerSel = req.session.controllers[0].name;
					}
					callback(null, data);
				});
		  },
		  function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/"+req.session.controllerSel+"/sensors_list";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					req.session.sensors = Array.from(data);
					if (typeof(req.session.sensorSel) == 'undefined') {
						req.session.sensorSel = req.session.sensors[0].id;
					}
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/"+req.session.controllerSel+"/"
				+req.session.sensorSel+"/"+req.session.datarange[0]+"/"+req.session.datarange[1]
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					callback(null, data);
				});
		  }
		],
		function (err, result) {
			res.render('pages/sensors.ejs', {
				url:  parseurl(req).pathname,
				controllers: req.session.controllers,
				sensors: req.session.sensors,
				controllerSel: req.session.controllerSel,
				sensorSel: req.session.sensorSel,
				measures: result[2]
			});
		});
  }
};