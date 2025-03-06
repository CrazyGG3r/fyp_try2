extends CharacterBody2D

@export var speed = 300
@export var kick_strength = 500
@export var min_kick_distance = 10.0  # Minimum distance to ensure consistent kicks
@export var rotation_amount = 60.0  # Degrees to rotate per key press
@export var kick_cooldown = 0.2  # seconds before allowing another kick

var can_kick = true
var kick_timer = 0.0

func _physics_process(delta):
	# Handle rotation
	if Input.is_key_pressed(KEY_RIGHT):
		rotation_degrees += rotation_amount * delta
	if Input.is_key_pressed(KEY_LEFT):
		rotation_degrees -= rotation_amount * delta
	
	# Get forward/backward input
	var forward_input = Input.get_axis("ui_down", "ui_up")  # Note: in Godot, positive Y is down
	
	# Calculate direction vector based on current rotation
	var direction = Vector2(0, -forward_input).rotated(rotation)
	
	# Set velocity based on direction and speed
	velocity = direction * speed
	
	# Move the player
	move_and_slide()
	
	# Handle kick cooldown timer
	if !can_kick:
		kick_timer += delta
		if kick_timer >= kick_cooldown:
			can_kick = true
			kick_timer = 0.0

# Use this function for dedicated kick areas (Areas2D)
# Use this function for direct body collision
func _on_fuck_it_2_body_entered(body):
	process_kick(body)

# Centralized kick processing
func process_kick(body):
	if !can_kick:
		return
		
	if body.is_in_group("ball"):
		# Calculate kick direction from player to ball
		var kick_vector = body.global_position - global_position
		
		# Ensure minimum distance for kick direction
		if kick_vector.length() < min_kick_distance:
			kick_vector = Vector2(0, -1).rotated(rotation) * min_kick_distance
		else:
			kick_vector = kick_vector.normalized() * min_kick_distance
		
		# Schedule the kick for the next frame to avoid physics conflicts
		call_deferred("apply_kick", body, kick_vector)
		
		# Set cooldown
		can_kick = false
		kick_timer = 0.0

# Apply kick on the next frame to avoid physics conflicts
func apply_kick(ball, kick_vector):
	ball.apply_central_impulse(kick_vector.normalized() * kick_strength)
