extends Node2D

var server := TCPServer.new()
var clients := []

func _ready():
	var err = server.listen(9999)
	if err == OK:
		print("Server listening on port 9999")
	else:
		print("Failed to bind to port 9999")

func _process(delta):
	# Accept new connections
	if server.is_connection_available():
		var client = server.take_connection()
		clients.append(client)
		print("New client connected")
	
	# Handle data from existing clients
	for client in clients:
		if client.get_status() == StreamPeerTCP.STATUS_CONNECTED:
			if client.get_available_bytes() > 0:
				var data = client.get_data(client.get_available_bytes())
				if data[0] == OK:
					var key = data[1].get_string_from_utf8()
					handle_key_input(key)
		else:
			clients.erase(client)
			print("Client disconnected")

func handle_key_input(key):
	print(key)
