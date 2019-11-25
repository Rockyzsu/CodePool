var http = require('http');

var server = http.createServer(function (req, res) {
    req.on('data', function(chunk) {
      console.log("Received notification:");
      console.log(chunk.toString());
    });
    
    req.on('end', function() {
      // empty 200 OK response for now
      res.writeHead(200, "OK", {'Content-Type': 'text/html'});
      res.end();
    });
});

server.listen(8000);
console.log("Server running at http://0.0.0.0:8000/");
