var express = require('express');
var mongoose = require('mongoose');
var bodyParse = require('body-parser');

var app = express();

app.use(express.static(__dirname));
app.use(bodyParse.json());
app.use(bodyParse.urlencoded({extended: false}));

mongoose.set('useUnifiedTopology', true);

var server = app.listen(3000, () => {
	console.log('server is running on port', server.address().port);
});

var io = require('socket.io').listen(server);


mongoose.connect("mongodb://localhost/group_chat",  {useNewUrlParser: true } , (err) => {
	console.log('mongodb connected', err);
});

var Message = mongoose.model('Message',{ name : String, message : String});


app.get('/messages', (req, res) => {
	Message.find({},(err, messages)=> {
    	res.send(messages);
  	});
});

app.post('/messages', (req, res) => {
	var message = new Message(req.body);
  	message.save((err) => {
	    if(err)
	    	sendStatus(500);
    	io.emit('message', req.body);
    	res.sendStatus(200);
  	});
});

io.on('connection', () => {
	console.log('a user is connected');
});