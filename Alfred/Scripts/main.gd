extends Node

var hexapod_server := TCPServer.new()
var ai_server := TCPServer.new()
var butler_server := TCPServer.new()

var clients = {
	"hexapod": null,
	"ai": null,
	"butler": null,
}

var waiting_for_hexapod = false

@onready var log_panel = $LogPanel

func _ready():
	hexapod_server.listen(1234)
	ai_server.listen(9999)
	butler_server.listen(5678)
	log_("Servers started.")

func _process(_delta):
	accept_connection(hexapod_server, "hexapod")
	accept_connection(ai_server, "ai")
	accept_connection(butler_server, "butler")
	poll_clients()

func accept_connection(server: TCPServer, role: String):
	if server.is_connection_available():
		var conn = server.take_connection()
		clients[role] = conn
		conn.set_no_delay(true)
		log_("%s connected." % role.capitalize())

func poll_clients():
	for role in clients.keys():
		var conn = clients[role]
		if conn and conn.get_available_bytes() > 0:
			var msg = conn.get_utf8_string(conn.get_available_bytes()).strip_edges()
			log_("%s: %s" % [role.capitalize(), msg])
			route_message(role, msg)

func route_message(sender: String, msg: String):
	if sender == "butler":
		if not waiting_for_hexapod and clients["ai"]:
			clients["ai"].put_utf8_string(msg + "\n")
			waiting_for_hexapod = true
			log_("Sent to AI: %s" % msg)
		else:
			log_("Ignored Butler msg: waiting for hexapod.")
	
	elif sender == "ai":
		if clients["hexapod"] and not waiting_for_hexapod:
			clients["hexapod"].put_utf8_string(msg + "\n")
			log_("Sent to Hexapod: %s" % msg)

	elif sender == "hexapod":
		log_("Hexapod: %s" % msg)
		waiting_for_hexapod = false
			

func log_(msg: String):
	var label = Label.new()
	label.text = msg
	log_panel.add_child(label)
	if log_panel.get_child_count() > 20:
		log_panel.get_child(0).queue_free()
