extends Node2D




#state vector send
#hexapodka distance and angle w.r.t ball.
# Called when the node enters the scene tree for the first time.
var state_vector = []
var states = 10
var flag_connected = 0

signal send_state_vector(state_vector)




func _ready():
	state_vector.resize(states)
	state_vector.fill(Vector2(0,0))

@onready var hexapodd = $"../hexapod"
@onready var ball = $"../Ball"
# Called every frame. 'delta' is the elapsed time since the previous frame.

func _process(delta):
	if flag_connected ==1:
		
		state_vector[0] = calculate_polar_coordinate(hexapodd)
		print(state_vector)
		print(flag_connected)
		send_state_vector.emit(state_vector)
	
	
func calculate_polar_coordinate(entity):
	var r = ball.balls[0].global_position.distance_to(entity.global_position)
	var theta = ball.balls[0].global_position.angle_to_point(entity.global_position)
	return Vector2(r,theta)


func _on_environment_connected():
	flag_connected = 1 # Replace with function body.
