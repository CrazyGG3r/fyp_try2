extends CharacterBody2D


const SPEED = 350.0
const angular_speed = deg_to_rad(20)
var movement = Vector2(0,0)

var fake_delta = null
func _physics_process(delta):
	if Input.is_action_just_pressed("BACKWARDS"):
		movement = Vector2(sin(rotation),cos(rotation)) * SPEED
		position += movement * delta
		#move_and_collide(movement)
	if Input.is_action_just_pressed("FORWARDS"):
		movement = Vector2( sin(rotation),-cos(rotation)) * SPEED
		position += movement * delta
		#move_and_collide(movement)
	if Input.is_action_just_pressed("RIGHT"):
		movement = Vector2( cos(rotation),sin(rotation)) * SPEED
		position += movement * delta
		#move_and_collide(movement)
	if Input.is_action_just_pressed("LEFT"):
		movement = Vector2( -cos(rotation),sin(rotation)) * SPEED
		position += movement * delta
		#move_and_collide(movement)
	if Input.is_action_just_pressed("RIGHT_ROTATE"):
		rotation += angular_speed 
		#move_and_collide(movement)
		
	if Input.is_action_just_pressed("LEFT_ROTATE"):
		rotation -= angular_speed 
		fake_delta = delta
		#move_and_collide(movement)
	move_and_slide()


func _on_environment_handel_action(action_str):
	if action_str == "FK":
		movement = Vector2( sin(rotation),-cos(rotation)) * SPEED
		position += movement * fake_delta
	if action_str == "BK":
		movement = Vector2(sin(rotation),cos(rotation)) * SPEED
		position += movement * fake_delta
	if action_str == "RT":
		movement = Vector2( cos(rotation),sin(rotation)) * SPEED
		position += movement * fake_delta
	if action_str == "LT":
		movement = Vector2( -cos(rotation),sin(rotation)) * SPEED
		position += movement * fake_delta
	if action_str == "R2":
		rotation += angular_speed 
	if action_str == "L2":
		rotation -= angular_speed
	
	
	print(action_str)
