extends CharacterBody2D
const SPEED = 350.0
const angular_speed = deg_to_rad(5)
var movement = Vector2(0,0)
var fake_delta = null
signal action()

var forward = Vector2(0, -1)  # Forward direction (up in local space)
var right = Vector2(1, 0)
func _physics_process(delta):
	#print(name)
	if Input.is_action_just_pressed("BACKWARDS"):
		movement = forward.rotated(rotation) * -SPEED
		move_and_collide(movement * delta)
	if Input.is_action_just_pressed("FORWARDS"):
		movement = forward.rotated(rotation) * SPEED
		move_and_collide(movement * delta)
	if Input.is_action_just_pressed("RIGHT"):
		movement = right.rotated(rotation) * SPEED
		move_and_collide(movement * delta)
	if Input.is_action_just_pressed("LEFT"):
		movement = right.rotated(rotation) * -SPEED
		move_and_collide(movement * delta)
	if Input.is_action_just_pressed("RIGHT_ROTATE"):
		rotation += angular_speed 
	if Input.is_action_just_pressed("LEFT_ROTATE"):
		rotation -= angular_speed
	fake_delta = delta
		
func reset():
	global_position = $"../Reset_positions/Hexapod".global_position
	global_rotation = deg_to_rad(90)

func _on_environment_handel_action(action_str):
	if action_str == "FK":
		movement = forward.rotated(rotation) * SPEED
		move_and_collide(movement*fake_delta)
		action.emit()
	if action_str == "BK":
		movement = forward.rotated(rotation) * -SPEED
		move_and_collide(-movement*fake_delta)
		action.emit()
	if action_str == "RT":
		movement = right.rotated(rotation) * SPEED
		move_and_collide(movement*fake_delta)
		action.emit()
	if action_str == "LT":
		movement = right.rotated(rotation) * -SPEED
		move_and_collide(movement*fake_delta)
		action.emit()
	if action_str == "R2":
		rotation += angular_speed 
		action.emit()
	if action_str == "L2":
		rotation -= angular_speed
		action.emit()
	print(action_str)


func _on_master_handler_handel_action(action_str):
	if action_str == "FK":
		movement = forward.rotated(rotation) * SPEED
		move_and_collide(movement*fake_delta)
		action.emit()
	if action_str == "BK":
		movement = forward.rotated(rotation) * -SPEED
		move_and_collide(-movement*fake_delta)
		action.emit()
	if action_str == "RT":
		movement = right.rotated(rotation) * SPEED
		move_and_collide(movement*fake_delta)
		action.emit()
	if action_str == "LT":
		movement = right.rotated(rotation) * -SPEED
		move_and_collide(movement*fake_delta)
		action.emit()
	if action_str == "R2":
		rotation += angular_speed 
		action.emit()
	if action_str == "L2":
		rotation -= angular_speed
		action.emit()
	print(action_str)
		
