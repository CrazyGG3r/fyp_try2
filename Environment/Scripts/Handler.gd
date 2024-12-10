extends Node2D

#episode ++
#reset object places
#update training stats
#save all training stats to a file after pressing stop
var episode_num = 0
var reward      = 0
var game_no     = 0


var episode_log = FileAccess.open("res://Data/episode_log.txt",FileAccess.READ_WRITE)
var training_number = FileAccess.open("res://Data/training_num.txt",FileAccess.READ)
var t_num = 0
signal nextep()
func _ready():
	t_num = int(training_number.get_as_text().strip_edges()) 
	var name_f = "res://Data/episode_log_"+str(t_num)+ ".txt"
	episode_log = FileAccess.open(name_f,FileAccess.WRITE)
	episode_log = FileAccess.open(name_f,FileAccess.READ_WRITE)
	t_num += 1
	training_number = FileAccess.open("res://Data/training_num.txt",FileAccess.WRITE)
	training_number.store_line(str(t_num))
	training_number.close()
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
	
signal handel_action(action)

func _on_butler_send_state_vector(state_vector):
	#print("from env:",state_vector)
	if environment.client_DQN and environment.client_DQN.get_status() ==2:
		var serialized_data = JSON.stringify(state_vector)
		print(serialized_data)
		var byte_state = serialized_data.to_utf8_buffer()
		environment.client_DQN.put_data(byte_state)
		get_tree().paused = true
		var data = environment.client_DQN.get_data(2)	
		if typeof(data) == TYPE_ARRAY and data.size() == 2:
			var byte_array = PackedByteArray(data[1])  # Extract the byte data
			var action_str = byte_array.get_string_from_utf8() # Convert to string
			print(action_str)
			handel_action.emit(action_str)
			get_tree().paused = false


