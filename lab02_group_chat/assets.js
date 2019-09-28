var socket = io();
var username, name;

$(() => {
    $("#send").click(()=>{
       	sendMessage({
        sender: username,
        receiver: $("#receiver").val(), 
        message:$("#message").val()});

        $("#receiver").val("");
        $("#message").val("");
    });
    getMessages();
});

$(() => {
    $("#submit").click( (e) => {
    	e.preventDefault();

        username = $("#username").val();
        name = $("#name").val();

        $(".pull-right").append("<p><h3>"+name+"</h3><small> @"+username+"</small></p>");
        $("#chat").show();
        $("#messages").show();

        $("#login").hide();

    	var formData = {'name': name, 'username': username};
    	socket.emit('register', formData);
	});
});


function addMessage(mess){
	$("#messages").append('<p><small>'+mess.time+'</small></p><h4><small>'+mess.type+'<small/> '+mess.name+'</h4> <p>'+mess.text+'</p>');
}

function getMessages(){
    var req = {'username': username};

	$.post('/get_messages', req, (data) => {
        $("#messages").empty();
   		data.forEach(addMessage);
   	});
}

function sendMessage(message){
	$.post('/messages', message);
}

socket.on('message', getMessages);