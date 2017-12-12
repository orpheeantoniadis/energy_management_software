define({ "api": [
  {
    "type": "post",
    "url": "/v0/radiator/write",
    "title": "Sends command to a radiator",
    "name": "command_radiator",
    "group": "Radiators",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "radiator_id",
            "description": "<p>Radiator ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "value",
            "description": "<p>Wished value</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Request-Exemple :     ",
          "content": "{\n   'radiator_id' : '1', \n   'value' : '200'\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "info",
            "description": "<p>Message confirming that the command was sent</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example of result in case of success: ",
          "content": "{   \n   \"info\": \"Command sent\"\n}",
          "type": "json"
        }
      ]
    },
    "description": "<p>Sends write command to a specific radiator. Value should be between 0 and 255</p>",
    "version": "0.0.0",
    "filename": "./KNX_REST_Server.py",
    "groupTitle": "Radiators"
  },
  {
    "type": "get",
    "url": "/v0/radiator/read/<radiator_id>",
    "title": "Reads Radiator's current value",
    "name": "read_radiator",
    "group": "Radiators",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "radiator_id",
            "description": "<p>Radiator ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "current_value",
            "description": "<p>current value</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example of result in case of success: ",
          "content": "{   \n  \"current_value\": \"120\"\n}",
          "type": "json"
        }
      ]
    },
    "description": "<p>Reads value of a specific radiator</p>",
    "version": "0.0.0",
    "filename": "./KNX_REST_Server.py",
    "groupTitle": "Radiators"
  },
  {
    "type": "post",
    "url": "/v0/store/write",
    "title": "Sends command to a store",
    "name": "command_store",
    "group": "Stores",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "store_id",
            "description": "<p>Store ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "value",
            "description": "<p>Wished value</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Request-Exemple :     ",
          "content": "{\n   'store_id' : '2', \n   'value' : '200'\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "info",
            "description": "<p>Message confirming that the command was sent</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example of result in case of success: ",
          "content": "{   \n   \"info\": \"Command sent\"\n}",
          "type": "json"
        }
      ]
    },
    "description": "<p>Sends write command to a specific store. Value should be between 0 and 255</p>",
    "version": "0.0.0",
    "filename": "./KNX_REST_Server.py",
    "groupTitle": "Stores"
  },
  {
    "type": "get",
    "url": "/v0/store/read/<store_id>",
    "title": "Reads Store's current value",
    "name": "read_store",
    "group": "Stores",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "store_id",
            "description": "<p>Store ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "current_value",
            "description": "<p>current value</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example of result in case of success: ",
          "content": "{   \n  \"current_value\": \"150\"\n}",
          "type": "json"
        }
      ]
    },
    "description": "<p>Reads value of a specific store</p>",
    "version": "0.0.0",
    "filename": "./KNX_REST_Server.py",
    "groupTitle": "Stores"
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "_root_Desktop_test_knx_doc_main_js",
    "groupTitle": "_root_Desktop_test_knx_doc_main_js",
    "name": ""
  }
] });
