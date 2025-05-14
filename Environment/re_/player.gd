# Player (Box) Script - Attach to your box node
extends CharacterBody2D

var speed = 200
var kick_strength = 300

func _physics_process(delta):
	# Get input direction
	var direction = Vector2.ZERO
	if Input.is_action_pressed("ui_right"):
		direction.x += 1
	if Input.is_action_pressed("ui_left"):
		direction.x -= 1
	if Input.is_action_pressed("ui_down"):
		direction.y += 1
	if Input.is_action_pressed("ui_up"):
		direction.y -= 1
	
	# Normalize for consistent speed in all directions
	if direction.length() > 0:
		direction = direction.normalized()
	
	# Set velocity and move
	velocity = direction * speed
	move_and_slide()
	
	# Kick the ball when space is pressed
	if Input.is_action_just_pressed("ui_accept"):  # Space bar
		kick_ball()

func kick_ball():
	# Find the ball in the scene
	var ball = get_node("../Ball")
	if ball and ball is RigidBody2D:
		# Calculate kick direction from player to ball
		var kick_direction = global_position.direction_to(ball.global_position)
		# Apply impulse force to the ball
		ball.apply_central_impulse(kick_direction * kick_strength)
