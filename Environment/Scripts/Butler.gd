extends Node2D




#state vector send
#hexapodka distance and angle w.r.t ball.
# Called when the node enters the scene tree for the first time.
var state_vector = []
var states = 25
var flag_connected = 1

signal send_state_vector(state_vector)




func _ready():
	state_vector.resize(states)
	state_vector.fill(0)
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
	if flag_connected == 1:
		var temp = Vector2.ZERO
		# Hexapod from ball
		temp = calculate_polar_coordinate(ball.ball, hexapodd)
		state_vector[0] = round(temp.x * 100) / 100.0
		state_vector[1] = round(temp.y * 100) / 100.0
		# wall_top from ball
		temp = Vector2(calculate_y_distance(ball.ball, wall_top) - 110, deg_to_rad(90))
		state_vector[2] = round(temp.x * 100) / 100.0
		state_vector[3] = round(temp.y * 100) / 100.0
		# wall_bottom from ball
		temp = Vector2(-(calculate_y_distance(ball.ball, wall_bot) - 110), deg_to_rad(270))
		state_vector[4] = round(temp.x * 100) / 100.0
		state_vector[5] = round(temp.y * 100) / 100.0
		# wall_right from ball
		temp = Vector2(-(calculate_x_distance(ball.ball, wall_right) - 110), deg_to_rad(0))
		state_vector[6] = round(temp.x * 100) / 100.0
		state_vector[7] = round(temp.y * 100) / 100.0
		# wall_left from ball
		temp = Vector2(calculate_x_distance(ball.ball, wall_left) - 110, deg_to_rad(180))
		state_vector[8] = round(temp.x * 100) / 100.0
		state_vector[9] = round(temp.y * 100) / 100.0
		# hexapod
		# wall_top from hexapodd
		temp = Vector2(calculate_y_distance(hexapodd, wall_top) - 110, deg_to_rad(90))
		state_vector[10] = round(temp.x * 100) / 100.0
		state_vector[11] = round(temp.y * 100) / 100.0
		# wall_bottom from hexapodd
		temp = Vector2(-(calculate_y_distance(hexapodd, wall_bot) - 110), deg_to_rad(270))
		state_vector[12] = round(temp.x * 100) / 100.0
		state_vector[13] = round(temp.y * 100) / 100.0
		# wall_right from hexapodd
		temp = Vector2(-(calculate_x_distance(hexapodd, wall_right) - 110), deg_to_rad(0))
		state_vector[14] = round(temp.x * 100) / 100.0
		state_vector[15] = round(temp.y * 100) / 100.0
		# wall_left from hexapodd
		temp = Vector2(calculate_x_distance(hexapodd, wall_left) - 110, deg_to_rad(180))
		state_vector[16] = round(temp.x * 100) / 100.0
		state_vector[17] = round(temp.y * 100) / 100.0
		# goal from ball
		temp = calculate_polar_coordinate(ball.ball, goal)
		state_vector[18] = round(temp.x * 100) / 100.0
		state_vector[19] = round(temp.y * 100) / 100.0
		# goal from hexapodd
		temp = calculate_polar_coordinate(hexapodd, goal)
		state_vector[20] = round(temp.x * 100) / 100.0
		state_vector[21] = round(temp.y * 100) / 100.0
		# reward
		state_vector[22] = round(master.reward * 100) / 100.0
		# timer
		temp = Vector2(timer.wait_time, timer.time_left)
		state_vector[23] = round(temp.x * 100) / 100.0
		state_vector[24] = round(temp.y * 100) / 100.0
		#for n in state_vector.size():
			#var a = state_vector[n]
			#state_vector[n] = a.round(2)
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
	
