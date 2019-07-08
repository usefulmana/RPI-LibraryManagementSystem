
app.get('/dashboard', function(req, res) {
  res.sendFile(path.join(__dirname + '/build/index.html'));
});

app.listen(9000);
