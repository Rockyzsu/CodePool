var express = require('express');
var app = express();

app.use(express.static('/usr/src/app/public'));

app.listen(process.env.PORT || 3000);
