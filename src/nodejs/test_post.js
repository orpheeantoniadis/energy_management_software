var Client = require('node-rest-client').Client;
var client = new Client();

var args = {
    data: { id: 1,d
            location: "A532",
            threshold: 10},

    headers: { "Content-Type": "application/json" }
};

client.post("http://localhost:5000/rules", args, function (data, response) {
    // parsed response body as js object
    console.log(data);
    // raw response
    console.log(response);
});

// registering remote methods
/*client.registerMethod("postMethod", "http://localhost:5000/rules", "POST");

client.methods.postMethod(args, function (data, response) {
    // parsed response body as js object
    console.log(data);
    // raw response
    console.log(response);
});*/
