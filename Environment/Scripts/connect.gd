extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


@onready var namee = $Fields/Name/Name_Input
@onready var port = $Fields/Port/Port_Input
@onready var ip = $Fields/IP/IP_Input



func _on_start_env_pressed():
	var portt = int (port.text)
	var ipp = str(ip.text)
	var nameee = str(namee.text)
	print(ipp,portt,nameee)
	Global.ip_address = ipp
	Global.port_number = portt
	Global.room_name = nameee
	
	get_tree().change_scene_to_file("res://Scenes/environment.tscn")
	
	
