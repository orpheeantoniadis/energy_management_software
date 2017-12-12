var parseurl = require('parseurl');
var async = require('async');
var Client = require('node-rest-client').Client;

var tempEmptySel = 1;
var tempFullSel = 1;
var humSel = 1;
var lumSel = 1;

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
  },
	
	getRoomAvg: function(req, res) {
		async.series([
		  function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/rooms_list";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					req.session.rooms = data.rooms;
					if (typeof(req.session.roomSel) == 'undefined') {
						req.session.roomSel = req.session.rooms[0];
					}
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/"+req.session.roomSel+"/nbMeasures";
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					req.session.nbMeasures = data.nbMeasures;
					if (typeof(req.session.nbMeasuresSel) == 'undefined') {
						req.session.nbMeasuresSel = 1;
					}
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/"+req.session.roomSel+"/average/"+req.session.nbMeasuresSel;
				client.registerMethod("jsonMethod", url, "GET");
				client.methods.jsonMethod(function (data, response) {
					callback(null, data);
				});
		  }
		],
		function (err, result) {
			res.render('pages/rooms.ejs', {
				url:  parseurl(req).pathname,
				rooms: req.session.rooms,
				roomSel: req.session.roomSel,
				nbMeasures: req.session.nbMeasures,
				nbMeasuresSel: req.session.nbMeasuresSel,
				measures: result[2],
				tempEmptySel: tempEmptySel,
				tempFullSel: tempFullSel,
				humSel: humSel,
				lumSel: lumSel
			});
		});
	},
	
	postDriversThresholds: function (req) {
		tempEmptySel = Number(req.body.tempEmpty);
		tempFullSel = Number(req.body.tempFull);
		humSel = Number(req.body.hum);
		lumSel = Number(req.body.lum);
		var rule1 = {
		    data: { rule: 1,
		            location: req.session.roomSel,
		            threshold: tempEmptySel},

		    headers: { "Content-Type": "application/json" }
		};
		var rule2 = {
		    data: { rule: 2,
		            location: req.session.roomSel,
		            threshold: tempFullSel},

		    headers: { "Content-Type": "application/json" }
		};
		var rule3 = {
		    data: { rule: 3,
		            location: req.session.roomSel,
		            threshold: humSel},

		    headers: { "Content-Type": "application/json" }
		};
		var rule4 = {
		    data: { rule: 4,
		            location: req.session.roomSel,
		            threshold: lumSel},

		    headers: { "Content-Type": "application/json" }
		};
		async.series([
		  function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/rules";
				client.registerMethod("postMethod", url, "POST");
				client.methods.postMethod(rule1, function (data, response) {
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/rules";
				client.registerMethod("postMethod", url, "POST");
				client.methods.postMethod(rule2, function (data, response) {
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/rules";
				client.registerMethod("postMethod", url, "POST");
				client.methods.postMethod(rule3, function (data, response) {
					callback(null, data);
				});
		  },
			function (callback) {
				var client = new Client();
				var url = "http://localhost:5000/rules";
				client.registerMethod("postMethod", url, "POST");
				client.methods.postMethod(rule4, function (data, response) {
					callback(null, data);
				});
		  }
		],
		function (err, result) {}
	);
  }
};