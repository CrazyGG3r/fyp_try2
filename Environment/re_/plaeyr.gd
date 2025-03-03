extends CharacterBody2D

@export var speed = 300
@export var kick_strength = 500

func _physics_process(delta):
	# Get player input
	var direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	# Set velocity based on direction and speed
	velocity = direction * speed
	
	# Move the player
	move_and_slide()

func _on_kick_area_body_entered(body):
	if body.is_in_group("ball"):
		# Calculate kick direction from player to ball
		var kick_direction = (body.global_position - global_position).normalized()
		# Apply impulse to the ball
		body.apply_central_impulse(kick_direction * kick_strength)
