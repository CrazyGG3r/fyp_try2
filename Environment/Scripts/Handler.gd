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
@onready var timer = $"../Game score/time/episode_Timer"


	
#episode end
func reset_epsiode():
	reset_field()
	goal = 0
	reward = 0
	timer.wait_time = 10
func reset_field():
	hexapod.reset()
	ball.reset()

var episode_log = FileAccess.open("res://Data/episode_log.txt",FileAccess.READ_WRITE)

func _on_episode_timer_timeout():
	var line = "ep: " + str(episode_num) + "\treward: " + str(reward) + "\ttimer: " + str("%.1f"%timer.wait_time) + "\tgoals: " + str(goal)
	episode_num += 1
	game_no += 1
	episode_log.seek_end()
	episode_log.store_line(line)
	reset_epsiode()


var goal = -1
signal re_timer()
func _on_goal_right_body_entered(body):
	if body.name == "hexapod":
		reward -= 100
	else:
		goal +=1 
		reward += 100
		re_timer.emit()
		reset_field()


signal start()

func _on_start_pressed():
	reset_epsiode()
	timer.wait_time = 10
	start.emit()


func _on_butler_send_state_vector(state_vector):
	#print("from env:",state_vector)
	if environment.client_DQN and environment.client_DQN.get_status() ==2:
		var serialized_data = JSON.stringify(state_vector)
		print(serialized_data)
		var byte_state = serialized_data.to_utf8_buffer()
		environment.client_DQN.put_data(byte_state)


