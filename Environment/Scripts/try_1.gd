extends RigidBody2D

@export var impulse_strength := 300.0
@export var torque_strength := 1000000.0
var reset_hexapod = null
var fake_delta = 0;
func _ready() -> void:
	reset_hexapod = get_parent().hex_reset
	inertia = 50.0  # Critical!
	angular_damp = 5.1  # Reduce if needed
	rotation = deg_to_rad(90)
	# Set physics properties
	linear_damp = 10.0
	position = reset_hexapod
	

func reset():
	linear_velocity = Vector2.ZERO
	inertia = 50
	rotation = deg_to_rad(90)
	position = reset_hexapod.global_position
	
func _physics_process(delta):
	if Input.is_action_just_pressed("FORWARDS"):
		var direction = Vector2.UP.rotated(rotation)
		apply_central_impulse(direction * impulse_strength)
	elif Input.is_action_just_pressed("BACKWARDS"):
		var direction = Vector2.DOWN.rotated(rotation)
		apply_central_impulse(direction * impulse_strength)
	if Input.is_action_just_pressed("LEFT_ROTATE"):
		apply_torque(-torque_strength * delta)
	elif Input.is_action_just_pressed("RIGHT_ROTATE"):
		apply_torque(torque_strength * delta)
	fake_delta = delta
func handle_action(action_str):
	match action_str:
		"FK":
			var direction = Vector2.UP.rotated(rotation)
			apply_central_impulse(direction * impulse_strength)
		"BK":
			var direction = Vector2.DOWN.rotated(rotation)
			apply_central_impulse(direction * impulse_strength)
		"L2":
			apply_torque(-torque_strength * fake_delta)
		"R2":
			apply_torque(-torque_strength * fake_delta)
