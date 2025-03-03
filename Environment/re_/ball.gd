extends RigidBody2D

@export var max_speed = 300
@export var friction = 0.98

func _ready():
	# Add ball to the "ball" group for easy reference
	add_to_group("ball")
	
	# Set physics properties
	gravity_scale = 0  # No gravity for top-down view
	linear_damp = 0.5  # Some damping to slow the ball naturally

func _integrate_forces(state):
	# Limit maximum speed
	if state.linear_velocity.length() > max_speed:
		state.linear_velocity = state.linear_velocity.normalized() * max_speed
	
	# Apply friction
	state.linear_velocity *= friction
