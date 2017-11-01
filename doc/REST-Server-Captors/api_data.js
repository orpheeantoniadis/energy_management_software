define({ "api": [  {    "type": "get",    "url": "/sensors/<node_id>/get_all_measures",    "title": "get_all_measures_sensor",    "name": "get_all_measures_sensor",    "group": "Sensors",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Number",            "optional": false,            "field": "node_id",            "description": "<p>Sensor's unique ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "controller",            "description": "<p>Controller name</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "location",            "description": "<p>Location of the sensor</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "sensor",            "description": "<p>Sensor's ID</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "battery",            "description": "<p>battery level (%)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "humidity",            "description": "<p>humidity level (%)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "luminance",            "description": "<p>luminance level (lux)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "temperature",            "description": "<p>temperature level (C)</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "motion",            "description": "<p>motion state (true or false)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "updateTime",            "description": "<p>Timestamp at the measures' reception</p>"          }        ]      },      "examples": [        {          "title": "Example of result in case of success:",          "content": "{\n    \"battery\": 100,\n    \"controller\": \"Pi lab1\",\n    \"humidity\": 22,\n    \"location\": \"Room A401\",\n    \"luminance\": 60,\n    \"motion\": false,\n    \"sensor\": 2,\n    \"temperature\": 30.0,\n    \"updateTime\": 1454682568\n}",          "type": "json"        }      ]    },    "description": "<p>Gets all measures of a given sensor, in a JSON format</p>",    "version": "0.0.0",    "filename": "./sensors-doc.py",    "groupTitle": "Sensors"  },  {    "type": "get",    "url": "/sensors/<node_id>/get_humidity",    "title": "get_humidity",    "name": "get_humidity",    "group": "Sensors",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Number",            "optional": false,            "field": "node_id",            "description": "<p>Sensor's unique ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "controller",            "description": "<p>Controller name</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "location",            "description": "<p>Location of the sensor</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "sensor",            "description": "<p>Sensor's ID</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "type",            "description": "<p>type of measurement</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "value",            "description": "<p>humidity level (%)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "updateTime",            "description": "<p>Timestamp at the measures' reception</p>"          }        ]      },      "examples": [        {          "title": "Example of result in case of success:",          "content": "{\n    \"controller\": \"Pi lab1\",\n    \"location\": \"Room A401\",\n    \"sensor\": 2,\n    \"type\": \"relative humidity\",\n    \"updateTime\": 1454682996,\n    \"value\": 21\n}",          "type": "json"        }      ]    },    "description": "<p>Gets humidity of a given sensor in a JSON format</p>",    "version": "0.0.0",    "filename": "./sensors-doc.py",    "groupTitle": "Sensors"  },  {    "type": "get",    "url": "/sensors/<node_id>/get_luminance",    "title": "get_luminance",    "name": "get_luminance",    "group": "Sensors",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Number",            "optional": false,            "field": "node_id",            "description": "<p>Sensor's unique ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "controller",            "description": "<p>Controller name</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "location",            "description": "<p>Location of the sensor</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "sensor",            "description": "<p>Sensor's ID</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "type",            "description": "<p>type of measurement</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "value",            "description": "<p>luminance level (lux)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "updateTime",            "description": "<p>Timestamp at the measures' reception</p>"          }        ]      },      "examples": [        {          "title": "Example of result in case of success:",          "content": "{\n    \"controller\": \"Pi lab1\",\n    \"location\": \"Room A401\",\n    \"sensor\": 2,\n    \"type\": \"luminance\",\n    \"updateTime\": 1454682996,\n    \"value\": 49\n}",          "type": "json"        }      ]    },    "description": "<p>Gets humidity of a given sensor in a JSON format</p>",    "version": "0.0.0",    "filename": "./sensors-doc.py",    "groupTitle": "Sensors"  },  {    "type": "get",    "url": "/sensors/<node_id>/get_motion",    "title": "get_motion",    "name": "get_motion",    "group": "Sensors",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Number",            "optional": false,            "field": "node_id",            "description": "<p>Sensor's unique ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "controller",            "description": "<p>Controller name</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "location",            "description": "<p>Location of the sensor</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "sensor",            "description": "<p>Sensor's ID</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "type",            "description": "<p>type of measurement</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "value",            "description": "<p>motion state (boolean)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "updateTime",            "description": "<p>Timestamp at the measures' reception</p>"          }        ]      },      "examples": [        {          "title": "Example of result in case of success:",          "content": "{\n    \"controller\": \"Pi lab1\",\n    \"location\": \"Room A401\",\n    \"sensor\": 2,\n    \"type\": \"sensor\",\n    \"updateTime\": 1454682996,\n    \"value\": true\n}",          "type": "json"        }      ]    },    "description": "<p>Gets motion of a given sensor in a JSON format</p>",    "version": "0.0.0",    "filename": "./sensors-doc.py",    "groupTitle": "Sensors"  },  {    "type": "get",    "url": "/sensors/get_sensors_list",    "title": "get_sensors_list",    "name": "get_sensors_list",    "group": "Sensors",    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String[]",            "optional": false,            "field": "JSON",            "description": "<p>List of all sensor nodes in the network i a JSON format</p>"          }        ]      },      "examples": [        {          "title": "Example of result in case of success:",          "content": "{\n    \"2\": \"MultiSensor 6\",\n    \"3\": \"MultiSensor 6\"\n}",          "type": "json"        }      ]    },    "description": "<p>Lists IDs and product names of all sensors nodes in the network. The controller is excluded.</p>",    "version": "0.0.0",    "filename": "./sensors-doc.py",    "groupTitle": "Sensors"  },  {    "type": "get",    "url": "/sensors/<node_id>/get_temperature",    "title": "get_temperature",    "name": "get_temperature",    "group": "Sensors",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Number",            "optional": false,            "field": "node_id",            "description": "<p>Sensor's unique ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "controller",            "description": "<p>Controller name</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "location",            "description": "<p>Location of the sensor</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "sensor",            "description": "<p>Sensor's ID</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "type",            "description": "<p>Type of measurement</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "value",            "description": "<p>Temperature level (C)</p>"          },          {            "group": "Success 200",            "type": "Number",            "optional": false,            "field": "updateTime",            "description": "<p>Timestamp of the measure</p>"          }        ]      },      "examples": [        {          "title": "Example of result in case of success:",          "content": "{\n    \"controller\": \"Pi lab1\",\n    \"location\": \"Room A401\",\n    \"sensor\": 2,\n    \"type\": \"temperature\",\n    \"updateTime\": 1454682568,\n    \"value\": 30.4\n}",          "type": "json"        }      ]    },    "description": "<p>Gets temperature of a given sensor in a JSON format</p>",    "version": "0.0.0",    "filename": "./sensors-doc.py",    "groupTitle": "Sensors"  }] });
