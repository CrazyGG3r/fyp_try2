extends Timer

# Called when the node enters the scene tree for the first time.
func _ready():
	wait_time = 3
	one_shot = false
	

signal tiemr_started()
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	

func _on_master_handler_start():
	start()


func _on_master_handler_re_timer():
	wait_time = time_left + 10
	start()
