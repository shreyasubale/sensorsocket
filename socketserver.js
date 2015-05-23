var zmq = require("zmq");
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var data = null;



app.get('/', function(req, res){
  res.sendfile('index.html');
});

sock = zmq.socket('sub');
sock.connect('tcp://127.0.0.1:5000');
sock.subscribe("distance1");



io.on('connection', function(socket){

	sock.on('message', function(message) {
	  var message = message.toString();
	  message = message.split(" ");
	  socket.emit('data', { 'sensor': message[1] });
	  //console.log(message.toString());
	});
  
});
http.listen(3000, function(){
  console.log('listening on *:3000');
});
