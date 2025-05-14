extends Node2D




#state vector send
#hexapodka distance and angle w.r.t ball.
# Called when the node enters the scene tree for the first time.
var state_vector = []
var states = 40
var flag_connected = 0

signal send_state_vector(state_vector)



@onready var master =$"../Master Handler"

@onready var hexapod_spawner: Node2D = $"../Hexapod_Spawner"
var hexapodd = null
@onready var obstacle_spawner: Node2D = $"../Obstacle spawner"
var obstacle = null
@onready var ball_spawner = $"../Ball_Spawner"
@onready var wall_top = $"../top/coll"
@onready var wall_bot =$"../bottom/coll"
@onready var wall_right = $"../right/coll"
@onready var wall_left =$"../left/coll"
@onready var goal =  $"../Goal_right/coll"
@onready var timer = $"../Game score/time/episode_Timer"
# Called every frame. 'delta' is the elapsed time since the previous frame.
var ball: RigidBody2D = null

func _ready():
	state_vector.resize(states)
	state_vector.fill(0)
	ball = ball_spawner.current_ball
	hexapodd = hexapod_spawner.current_hexapod
	obstacle = obstacle_spawner.current_obstacle
var done =  0

func _process(delta):
	if not obstacle and obstacle_spawner.current_obstacle:
		obstacle = obstacle_spawner.current_obstacle
	if not obstacle:
		return
	if not hexapodd and hexapod_spawner.current_hexapod:
		hexapodd = hexapod_spawner.current_hexapod
	if not hexapodd:
		return

	if not ball and ball_spawner.current_ball:
		ball = ball_spawner.current_ball
	if not ball:
		return
		
	if flag_connected == 1:
			var temp = Vector2.ZERO
			# ball_hexapod
			temp = calculate_polar_coordinate(ball, hexapodd)
			state_vector[0] = round(temp.x * 100) / 100.0
			state_vector[1] = round(temp.y * 100) / 100.0
			# ball_obstacle
			temp = calculate_polar_coordinate(ball,obstacle)
			state_vector[2] = round(temp.x * 100) / 100.0
			state_vector[3] = round(temp.y * 100) / 100.0
			# ball_goal
			temp = calculate_polar_coordinate(ball,goal)
			state_vector[4] = round(temp.x * 100) / 100.0
			state_vector[5] = round(temp.y * 100) / 100.0
			# ball_top
			temp = Vector2(calculate_y_distance(ball, wall_top) - 110, deg_to_rad(90))
			state_vector[6] = round(temp.x * 100) / 100.0
			state_vector[7] = round(temp.y * 100) / 100.0
			# ball_bottom
			temp = Vector2(-(calculate_y_distance(ball, wall_bot) - 110), deg_to_rad(270))
			state_vector[8] = round(temp.x * 100) / 100.0
			state_vector[9] = round(temp.y * 100) / 100.0
			#ball_left
			temp = Vector2(calculate_x_distance(ball, wall_left) - 110, deg_to_rad(180))
			state_vector[10] = round(temp.x * 100) / 100.0
			state_vector[11] = round(temp.y * 100) / 100.0
			#ball_right
			temp = Vector2(-(calculate_x_distance(ball, wall_right) - 110), deg_to_rad(0))
			state_vector[12] = round(temp.x * 100) / 100.0
			state_vector[13] = round(temp.y * 100) / 100.0
			# hexapod
			#hexapod_obstacle
			temp = calculate_polar_coordinate(hexapodd,obstacle)
			state_vector[14] = round(temp.x * 100) / 100.0
			state_vector[15] = round(temp.y * 100) / 100.0
			#hexapod_goal
			temp = calculate_polar_coordinate(hexapodd,goal)
			state_vector[16] = round(temp.x * 100) / 100.0
			state_vector[17] = round(temp.y * 100) / 100.0
			# wall_top from hexapodd
			temp = Vector2(calculate_y_distance(hexapodd, wall_top) - 110 , deg_to_rad(90))
			state_vector[18] = round(temp.x * 100) / 100.0
			state_vector[19] = round(temp.y * 100) / 100.0
			# wall_bottom from hexapodd
			temp = Vector2(-(calculate_y_distance(hexapodd, wall_bot) - 110), deg_to_rad(270))
			state_vector[20] = round(temp.x * 100) / 100.0
			state_vector[21] = round(temp.y * 100) / 100.0
			# wall_left from hexapodd
			temp = Vector2(calculate_x_distance(hexapodd, wall_left) - 110, deg_to_rad(180))
			state_vector[22] = round(temp.x * 100) / 100.0
			state_vector[23] = round(temp.y * 100) / 100.0
			# wall_right from hexapodd
			temp = Vector2(-(calculate_x_distance(hexapodd, wall_right) - 110), deg_to_rad(0))
			state_vector[24] = round(temp.x * 100) / 100.0
			state_vector[25] = round(temp.y * 100) / 100.0
			# obstacle_goal
			temp = calculate_polar_coordinate(obstacle, goal)
			state_vector[26] = round(temp.x * 100) / 100.0
			state_vector[27] = round(temp.y * 100) / 100.0
			#obstacle_top
			temp = Vector2(calculate_y_distance(obstacle, wall_top) - 110, deg_to_rad(90))
			state_vector[28] = round(temp.x * 100) / 100.0
			state_vector[29] = round(temp.y * 100) / 100.0
			# obstacle_bottom
			temp = Vector2(-(calculate_y_distance(obstacle, wall_bot) - 110), deg_to_rad(270))
			state_vector[30] = round(temp.x * 100) / 100.0
			state_vector[31] = round(temp.y * 100) / 100.0
			#obstacle_left
			temp = Vector2(calculate_x_distance(obstacle, wall_left) - 110, deg_to_rad(180))
			state_vector[32] = round(temp.x * 100) / 100.0
			state_vector[33] = round(temp.y * 100) / 100.0
			#obstacle_right
			temp = Vector2(-(calculate_x_distance(obstacle, wall_right) - 110), deg_to_rad(0))
			state_vector[34] = round(temp.x * 100) / 100.0
			state_vector[35] = round(temp.y * 100) / 100.0
			#timer - total_time, time_left
			temp = Vector2(timer.wait_time, timer.time_left)
			state_vector[36] = round(temp.x * 100) / 100.0
			state_vector[37] = round(temp.y * 100) / 100.0
			# done_and_reward 
			if done == 1:
				state_vector[38] = done
				done = 0
			else:
				state_vector[38] = done
			cal_reward()
			state_vector[39] = round(master.reward * 100) / 100.0
			send_state_vector.emit(state_vector)
			timer.paused = false
	

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
	print("CONNNECTEDDDD	")


func _on_hexapod_action():
	master.reward += 0.1 #reward on taking action
	
var prev_goal = 0

func _on_each_second_timeout():
	if prev_goal == master.goal:
		master.reward	-= 2 #to encourage faster goal 
		
	
func _on_episode_timer_timeout():
	done = 1
	timer.paused = false

func _on_episode_timer_tiemr_started():
	done = 0

func cal_reward():
	if is_moving_towards_goal(hexapodd, goal, hexapodd.linear_velocity):
		master.reward += 2
	if is_moving_towards_goal(ball, goal, ball.linear_velocity):
		master.reward += 2

	
	if calculate_polar_coordinate(hexapodd,obstacle).x < 50:
		master.reward -= 1
	if calculate_polar_coordinate(hexapodd,ball).x < 100:
		master.reward += 0.001
	#print(calculate_y_distance(hexapodd,wall_top))
	if calculate_y_distance(hexapodd,wall_top)< 170.0:
		#print("top")
		master.reward -= 0.002
	#print(calculate_y_distance(wall_bot,hexapodd))
	if calculate_y_distance(wall_bot,hexapodd)< 170.0:
		#print("bottom")
		master.reward -= 0.002
	#print(calculate_x_distance(wall_right,hexapodd))
	if calculate_x_distance(wall_right,hexapodd)< 172.0:
		#print("right")
		master.reward -= 0.002
	#print(calculate_x_distance(hexapodd,wall_left))
	if calculate_x_distance(hexapodd,wall_left)< 170.0:
		#print("left")
		master.reward -= 0.002
func is_moving_towards_goal(entity, goal, velocity) -> bool:
	var to_goal = (goal.global_position - entity.global_position).normalized()
	var direction = velocity.normalized()
	return to_goal.dot(direction) > 0.7
