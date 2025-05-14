extends RigidBody2D

const THRUST = 350.0
const SPEED = 350.0
const TORQUE = 5000.0  # Rotational force
signal action()

# Movement variables
var forward = Vector2(0, -1)  # Forward direction (up in local space)
var right = Vector2(1, 0)     # Right direction
var fake_delta = null

# Export variables for tweaking in the editor
@export var push_force: float = 500.0  # Force applied when colliding
@export var MAX_VELOCITY: float = 100.0
@export var min_velocity: float = 0.0
# Angular damping for rotation friction

func _ready() -> void:
	# Set initial rotation
	rotation = deg_to_rad(0)
	# Set physics properties
	linear_damp = 1.0
	angular_damp = 0.5
	contact_monitor = true  # Enable contact monitoring for collision detection
	max_contacts_reported = 4  # Allow reporting of multiple contacts

func _physics_process(delta):
	# Handle rotation
	#if Input.is_action_pressed("ui_right"):
		#apply_torque(TORQUE)
	#elif Input.is_action_pressed("ui_left"):
		#apply_torque(-TORQUE)
	
	# Handle movement relative to object orientation
	#var movement_impulse = Vector2.ZERO
	#
	#if Input.is_action_pressed("FORWARDS"):
		#movement_impulse += Vector2.UP.rotated(rotation) * THRUST * delta
	#if Input.is_action_pressed("BACKWARDS"):
		#movement_impulse += Vector2.DOWN.rotated(rotation) * THRUST * delta
	#
	## Apply movement
	#if movement_impulse != Vector2.ZERO:
		#apply_central_impulse(movement_impulse)
	#
	# Clamp velocity
	linear_velocity = linear_velocity.limit_length(MAX_VELOCITY)
func reset():
	# Reset position and rotation
	global_position = $"../Reset_positions/Hexapod".global_position
	rotation = deg_to_rad(90)
	# Reset physics
	linear_velocity = Vector2.ZERO
	angular_velocity = 0



# Common action handling for both environment and master
func handle_action(action_str):
	match action_str:
		"FK":
			# Apply forward impulse
			apply_central_impulse(forward.rotated(rotation) * SPEED * fake_delta)
			action.emit()
		"BK":
			# Apply backward impulse
			apply_central_impulse(-forward.rotated(rotation) * SPEED * fake_delta)
			action.emit()

		"R2":
			# Apply clockwise torque
			apply_torque(TORQUE * fake_delta)
			action.emit()
		"L2":
			# Apply counter-clockwise torque
			apply_torque(-TORQUE * fake_delta)
			action.emit()
	
	print(action_str)
