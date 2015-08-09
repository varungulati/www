var express = require('express');

var app = express();

app.use(express.static(__dirname + '/solid/theme'));
app.use("/partials", express.static(__dirname + '/solid/theme/assets/partials/'));

app.listen(3000);
console.log('Server running on port 3000');
