var Client = require('node-rest-client').Client;
var client = new Client();

/*var args = {
    data: { rule: 3,
            location: "A401",
            threshold: 221},

    headers: { "Content-Type": "application/json" }
};*/

var args = {
    data: { rule: 2,
            location: "A501",
            threshold: 15},

    headers: { "Content-Type": "application/json" }
};

client.post("http://localhost:5000/rules", args, function (data, response) {
    // parsed response body as js object
    console.log(data);
    // raw response
    console.log(response);
});

// registering remote methods
client.registerMethod("postMethod", "http://localhost:5000/rules", "POST");

client.methods.postMethod(args, function (data, response) {
    // parsed response body as js object
    console.log(data);
    // raw response
    //console.log(response);
});
