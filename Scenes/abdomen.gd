extends CharacterBody2D

@export var speed = 200  # Pixels per second

func _physics_process(delta):
	# Get input direction
	var input_direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	# Calculate velocity
	velocity = input_direction * speed
	
	# Move and slide will handle collision
	move_and_slide()

func _on_body_entered(body):
	if body.is_in_group("ball"):
		# Handle collision with ball
		var collision_force = velocity * 2  # Increased force, adjust as needed
		body.apply_central_impulse(collision_force)
	elif body.is_in_group("goal"):
		# Handle collision with goal (e.g., prevent entering)
		pass  # Implement goal interaction if needed
