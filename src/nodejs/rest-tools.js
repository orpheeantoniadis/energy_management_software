var parseurl = require('parseurl');
var async = require('async');
var Client = require('node-rest-client').Client;

var tempEmptySel = new Map();
var tempFullSel = new Map();
var humSel = new Map();
var lumSel = new Map();

var radiators = [];
var stores = [];

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
			req.session.rooms.forEach(function(room, index) {
				if (typeof(tempEmptySel.get(room)) == 'undefined') {
					tempEmptySel.set(room, 1);
					tempFullSel.set(room, 1);
					humSel.set(room, 1);
					lumSel.set(room, 1);
				}
			});
			res.render('pages/rooms.ejs', {
				url:  parseurl(req).pathname,
				rooms: req.session.rooms,
				roomSel: req.session.roomSel,
				nbMeasures: req.session.nbMeasures,
				nbMeasuresSel: req.session.nbMeasuresSel,
				measures: result[2],
				tempEmptySel: tempEmptySel.get(req.session.roomSel),
				tempFullSel: tempFullSel.get(req.session.roomSel),
				humSel: humSel.get(req.session.roomSel),
				lumSel: lumSel.get(req.session.roomSel),
				radiators: radiators,
				stores: stores
			});
		});
	},
	
	postDriversThresholds: function (req) {
		tempEmptySel.set(req.session.roomSel, Number(req.body.tempEmpty));
		tempFullSel.set(req.session.roomSel, Number(req.body.tempFull));
		humSel.set(req.session.roomSel, Number(req.body.hum));
		lumSel.set(req.session.roomSel, Number(req.body.lum));
		var rule1 = {
		    data: { 
					rule: 1,
          location: req.session.roomSel,
          threshold: tempEmptySel.get(req.session.roomSel)
				},
		    headers: { "Content-Type": "application/json" }
		};
		var rule2 = {
		    data: { 
					rule: 2,
          location: req.session.roomSel,
          threshold: tempFullSel.get(req.session.roomSel)
				},
		    headers: { "Content-Type": "application/json" }
		};
		var rule3 = {
		    data: {
					rule: 3,
          location: req.session.roomSel,
          threshold: humSel.get(req.session.roomSel)
				},
		    headers: { "Content-Type": "application/json" }
		};
		var rule4 = {
		    data: { 
					rule: 4,
          location: req.session.roomSel,
          threshold: lumSel.get(req.session.roomSel)
				},
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
		function (err, result) {});
	},
	
	setDrivers: function (drivers) {
		Object.keys(drivers).forEach(function(key, index) {
			var device = Object.getOwnPropertyDescriptor(drivers, key).value;
			if (device.type == 'radiator') {
				radiators.push(device);
			} else if (device.type == 'store') {
				stores.push(device);
			}
		});
	},
	
	getRadiatorsValues: function () {
		radiators.forEach(function(radiator, index) {
			var client = new Client();
			var url = "http://localhost:5000/v0/radiator/read/"+radiator.id;
			client.registerMethod("jsonMethod", url, "GET");
			client.methods.jsonMethod(function (data, response) {
				radiator.value = data.current_value;
			});
		});
  },
	
	getStoresValues: function () {
		stores.forEach(function(store, index) {
			var client = new Client();
			var url = "http://localhost:5000/v0/store/read/"+store.id;
			client.registerMethod("jsonMethod", url, "GET");
			client.methods.jsonMethod(function (data, response) {
				store.value = data.current_value;
			});
		});
  }
};