const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'build')));

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname + '/build/index.html'));
});

app.get('/login', function(req, res) {
  res.sendFile(path.join(__dirname + '/build/index.html'));
});

app.get('/dashboard', function(req, res) {
  res.sendFile(path.join(__dirname + '/build/index.html'));
});
app.get('/reports', function(req, res) {
  res.sendFile(path.join(__dirname + '/build/index.html'));
});
app.get('/search/:query?', function(req, res) {
  res.sendFile(path.join(__dirname + '/build/index.html'));
});
PORT = 9000
console.log(`Web server is running on port ${PORT}`)
app.listen(PORT);
