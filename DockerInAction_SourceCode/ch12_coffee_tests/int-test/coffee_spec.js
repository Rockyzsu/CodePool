var frisby = require('frisby');
frisby.create('ping test')
  .get('http://coffee_1:3000/api/ping')
  .expectStatus(200)
.toss();
