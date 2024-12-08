extends Node2D




#state vector send
#hexapodka distance and angle w.r.t ball.
# Called when the node enters the scene tree for the first time.
var state_vector = []
var states = 10
var flag_connected = 1

signal send_state_vector(state_vector)




func _ready():
	state_vector.resize(states)
	state_vector.fill(Vector2(0,0))

@onready var hexapodd = $"../hexapod"
@onready var ball = $"../ball_"
@onready var wall_top = $"../top/coll"
@onready var wall_bot =$"../bottom/coll"
@onready var wall_right = $"../right/coll"
@onready var wall_left =$"../left/coll"
# Called every frame. 'delta' is the elapsed time since the previous frame.

func _process(delta):
	if flag_connected ==1:
		
		# Hexapod from ball
		state_vector[0] = calculate_polar_coordinate(hexapodd)
		# wall_top from ball
		state_vector[1] = Vector2(calculate_y_distance(wall_top)-110,deg_to_rad(90))
		#wall_bottom from ball
		state_vector[2] = Vector2(-(calculate_y_distance(wall_bot)-110),deg_to_rad(270))
		#wall_right from ball
		state_vector[3] = Vector2(-(calculate_x_distance(wall_right)-110),deg_to_rad(0))
		#wall_left from ball
		state_vector[4] = Vector2(calculate_x_distance(wall_left)-110,deg_to_rad(180))
		
		
		send_state_vector.emit(state_vector)
	
func calculate_polar_coordinate(entity):
	var r = ball.ball.global_position.distance_to(entity.global_position)
	var theta = ball.ball.global_position.angle_to_point(entity.global_position)
	return Vector2(r,theta)

func calculate_y_distance(static_entity):
	var d = ball.ball.global_position.y - static_entity.global_position.y
	return d	
	
func calculate_x_distance(static_entity):
	var d = ball.ball.global_position.x - static_entity.global_position.x
	return d	
	
func _on_environment_connected():
	flag_connected = 1 # Replace with function body.
