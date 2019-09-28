var express = require('express');
var bodyParse = require('body-parser');

var app = express();

app.use(express.static(__dirname));
app.use(bodyParse.json());
app.use(bodyParse.urlencoded({extended: false}));


var server = app.listen(3000, () => {
	console.log('server is running on port', server.address().port);
});

var io = require('socket.io').listen(server);


var connectedUsers = {};
var messages = {};

app.post('/get_messages', (req, res) => {

	if(req.body.username){
		l_messages = messages[req.body.username];
		res.send(l_messages.reverse());
	}
});

app.post('/messages', (req, res) => {
	var receiver = req.body.receiver.trim();
	var sender = req.body.sender.trim();

	messages[receiver].push({'name': connectedUsers[sender].name, 'text': req.body.message, 'type': "From: ", 'time': new Date().toGMTString()});
	messages[sender].push({'name': connectedUsers[receiver].name, 'text': req.body.message, 'type': "To: ", 'time': new Date().toGMTString()});

	io.emit('message');
});

io.on('connection', (socket) => {
	socket.on('register', (data, res) => {
		if(!connectedUsers.hasOwnProperty(data.username)){
			connectedUsers[data.username] = {name: data.name};
			var username = data.username.trim()
			messages[username] = [];
		}
	});
});