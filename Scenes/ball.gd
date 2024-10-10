extends RigidBody2D

@export var friction = 0.5  # Adjust this to control how quickly the ball slows down
@export var max_speed = 500 # set after testing real ball

func _ready():
	# Add the ball to the "ball" group
	add_to_group("ball")
	
	# Set up physics for top-down view
	gravity_scale = 0  # No gravity
	linear_damp = friction  # Apply friction to slow the ball down over time

func _physics_process(delta):
	# Limit the ball's speed
	if linear_velocity.length() > max_speed:
		linear_velocity = linear_velocity.normalized() * max_speed

func _on_body_entered(body):
	if body is CharacterBody2D:  # Assuming the player is a CharacterBody2D
		# The player script now handles applying force to the ball
		print("Ball hit by player!")

# Optional: Add a method to reset the ball's position
func reset_position(pos: Vector2):
	global_position = pos
	linear_velocity = Vector2.ZERO
	angular_velocity = 0.0
