var http = require('http');

var server = http.createServer(function (req, res) {
    req.on('data', function(chunk) {
      console.log("Received notification:");
      var raw = chunk.toString();
      console.log(raw);
      var eventListBlob = JSON.parse(raw);
      
      for (var i = 0; i < eventListBlob.events.length; i++) {
        if (eventListBlob.events[i].target.mediaType != "application/vnd.docker.distribution.manifest.v1+json") {
          continue;
        }

        var data = JSON.stringify(eventListBlob.events[i]);
        var options = {
          hostname: 'esnode',
          port: 9200,
          path: '/registry-events/event/' + eventListBlob.events[i].id,
          method: 'PUT',
          headers: {
            'Content-Length': data.length
          }
        };

        var req = http.request(options, function(res){
          console.log('STATUS: ' + res.statusCode);
          console.log('HEADERS: ' + JSON.stringify(res.headers));
          res.setEncoding('utf8');
          res.on('data', function (chunk) {
            console.log('BODY: ' + chunk);
          });
        });
        req.write(data);
        req.end();
      }
    });
    
    req.on('end', function() {
      // empty 200 OK response for now
      res.writeHead(200, "OK", {'Content-Type': 'text/html'});
      res.end();
    });
});

server.listen(8000);
console.log("Server running at http://0.0.0.0:8000/");
