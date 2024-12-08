extends Node2D

#episode ++
#reset object places
#update training stats
#save all training stats to a file after pressing stop
var episode_num = 0
var reward      = 0
var game_no     = 0


signal nextep()
func _ready():
	pass # Replace with function body.
func _process(delta):
	pass

@onready var environment = $".."
@onready var hexapod = $"../hexapod"
@onready var ball = $"../ball_"

#positions
@onready var hexpositions =$"../Reset_positions/Hexapod"
@onready var ballpos = $"../Reset_positions/Ball"
#episode end
func reset_epsiode():
	hexapod.reset()
	ball.reset()
	goal = 0
	
func _on_episode_timer_timeout():
	reset_epsiode()


var goal = 0

func _on_goal_right_body_entered(body):
	goal +=1 
	print(goal)

signal start()
func _on_start_pressed():
	reset_epsiode()
	start.emit()


func _on_butler_send_state_vector(state_vector):
	#print("from env:",state_vector)
	if environment.client_DQN and environment.client_DQN.get_status() ==2:
		var serialized_data = JSON.stringify(state_vector)
		print(serialized_data)
		var byte_state = serialized_data.to_utf8_buffer()
		environment.client_DQN.put_data(byte_state)


