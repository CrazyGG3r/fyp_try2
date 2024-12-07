extends Node2D

var server = TCPServer.new()
var client_DQN = server.take_connection()
signal handel_action(action_str)
signal connected()
signal start()
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
			connected.emit()
	
	# Read data from the client if available
	if client_DQN and client_DQN.get_available_bytes() > 0:
		var data = client_DQN.get_data(2)	
		if typeof(data) == TYPE_ARRAY and data.size() == 2:
			var byte_array = PackedByteArray(data[1])  # Extract the byte data
			var action_str = byte_array.get_string_from_utf8() # Convert to string
			#print(action_str)
			handel_action.emit(action_str)







func _on_butler_send_state_vector(state_vector):
	pass # Replace with function body.
