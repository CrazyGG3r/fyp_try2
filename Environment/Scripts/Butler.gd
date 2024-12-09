extends Node2D




#state vector send
#hexapodka distance and angle w.r.t ball.
# Called when the node enters the scene tree for the first time.
var state_vector = []
var states = 14
var flag_connected = 1

signal send_state_vector(state_vector)




func _ready():
	state_vector.resize(states)
	state_vector.fill(Vector2(0,0))
@onready var master =$"../Master Handler"
@onready var hexapodd = $"../hexapod"
@onready var ball = $"../ball_"
@onready var wall_top = $"../top/coll"
@onready var wall_bot =$"../bottom/coll"
@onready var wall_right = $"../right/coll"
@onready var wall_left =$"../left/coll"
@onready var goal =  $"../Goal_right/coll"
@onready var timer = $"../Game score/time/episode_Timer"
# Called every frame. 'delta' is the elapsed time since the previous frame.

func _process(delta):
	if flag_connected ==1:
		# Hexapod from ball
		state_vector[0] = calculate_polar_coordinate(ball.ball,hexapodd)
		# wall_top from ball
		state_vector[1] = Vector2(calculate_y_distance(ball.ball,wall_top)-110,deg_to_rad(90))
		#wall_bottom from ball
		state_vector[2] = Vector2(-(calculate_y_distance(ball.ball,wall_bot)-110),deg_to_rad(270))
		#wall_right from ball
		state_vector[3] = Vector2(-(calculate_x_distance(ball.ball,wall_right)-110),deg_to_rad(0))
		#wall_left from ball
		state_vector[4] = Vector2(calculate_x_distance(ball.ball,wall_left)-110,deg_to_rad(180))
		#hexapod
		#state_vector[0] = calculate_polar_coordinate(ball.ball,hexapodd)
		#wall_top from hexapodd
		state_vector[5] = Vector2(calculate_y_distance(hexapodd,wall_top)-110,deg_to_rad(90))
		#wall_bottom from hexapodd
		state_vector[6] = Vector2(-(calculate_y_distance(hexapodd,wall_bot)-110),deg_to_rad(270))
		#wall_right from hexapodd
		state_vector[7] = Vector2(-(calculate_x_distance(hexapodd,wall_right)-110),deg_to_rad(0))
		#wall_left from ball
		state_vector[8] = Vector2(calculate_x_distance(hexapodd,wall_left)-110,deg_to_rad(180))
		#goal from ball
		state_vector[9] = calculate_polar_coordinate(ball.ball,goal)
		#goal from hexapodd
		state_vector[10] = calculate_polar_coordinate(hexapodd,goal)
		#reward
		state_vector[11] = master.reward
		#timer
		state_vector[13] = Vector2(timer.wait_time,timer.time_left)
		
		
		send_state_vector.emit(state_vector)
		
func calculate_polar_coordinate(entity1,entity2):
	var r = entity1.global_position.distance_to(entity2.global_position)
	var theta = entity1.global_position.angle_to_point(entity2.global_position)
	return Vector2(r,theta)

func calculate_y_distance(entity,static_entity):
	var d = entity.global_position.y - static_entity.global_position.y
	return d	
	
func calculate_x_distance(entity,static_entity):
	var d = entity.global_position.x - static_entity.global_position.x
	return d	
	
func _on_environment_connected():
	flag_connected = 1 # Replace with function body.


func _on_hexapod_action():
	master.reward += 0.1 #reward on taking action

var prev_goal = 0

func _on_each_second_timeout():
	if prev_goal == master.goal:
		master.reward	-= 5
	
