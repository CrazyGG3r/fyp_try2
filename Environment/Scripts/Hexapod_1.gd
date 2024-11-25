extends RigidBody2D


const SPEED = 300.0
const angular_speed = deg_to_rad(20)
var movement = Vector2(0,0)
func _physics_process(delta):
	if Input.is_action_just_pressed("BACKWARDS"):
		movement = Vector2(sin(rotation),cos(rotation)) * SPEED
		position += movement * delta
	if Input.is_action_just_pressed("FORWARDS"):
		movement = Vector2( sin(rotation),-cos(rotation)) * SPEED
		position += movement * delta
	if Input.is_action_just_pressed("RIGHT"):
		movement = Vector2( cos(rotation),sin(rotation)) * SPEED
		position += movement * delta
	if Input.is_action_just_pressed("LEFT"):
		movement = Vector2( -cos(rotation),sin(rotation)) * SPEED
		position += movement * delta
	if Input.is_action_just_pressed("RIGHT_ROTATE"):
		rotation += angular_speed 
	if Input.is_action_just_pressed("LEFT_ROTATE"):
		rotation -= angular_speed 
		
