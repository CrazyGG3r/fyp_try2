extends Node2D

var server = TCPServer.new()
var client_DQN = server.take_connection()
signal handel_action(action_str)

func _ready():
	print("IP Address:", Global.ip_address)
	print("Room Name:", Global.room_name)
	print("Port Number:", Global.port_number)
	var result = server.listen(Global.port_number, Global.ip_address)
	if result == OK:
		print("Server is listening on port", Global.port_number)
	else:
		print("Failed to start server:", result)

func _process(delta):
	# Check for new client connections
	if server.is_connection_available():
		client_DQN = server.take_connection()
		if client_DQN:
			client_DQN.set_no_delay(true)
			print("New client connected.")
	
	# Read data from the client if available
	if client_DQN and client_DQN.get_available_bytes() > 0:
		var data = client_DQN.get_data(2)	
		if typeof(data) == TYPE_ARRAY and data.size() == 2:
			var byte_array = PackedByteArray(data[1])  # Extract the byte data
			var action_str = byte_array.get_string_from_utf8() # Convert to string
			handel_action.emit(action_str)
			#print("Received action:", action_str)
			#handle_action(action_str)
		#var te = action[1].get_string_from_utf8()
		#print("Received action:", action)
		#handle_action(action)


#func handle_action(action):
	## Handle the received action
	#print("Handling action:", action)

