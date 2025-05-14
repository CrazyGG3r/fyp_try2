extends Node2D

@export var hexapod_scene: PackedScene
@onready var hexapod_spawn_point: Marker2D = $"../Reset_positions/Hexapod" # Changed name for clarity
@onready var ball_spawner: Node2D = $"../Ball_Spawner"

var current_hexapod: RigidBody2D = null
var hex_reset = null
var ball_spawn = null
func _ready() -> void:
	ball_spawn = ball_spawner
	hex_reset = hexapod_spawn_point.global_position
	call_deferred("spawn_hexapod")

func spawn_hexapod() -> void:
	if current_hexapod:
		current_hexapod.queue_free()
		current_hexapod = null

	if hexapod_scene != null:
		var new_hexapod = hexapod_scene.instantiate()
		new_hexapod.global_position = hexapod_spawn_point.global_position
		add_child(new_hexapod)
		#  No need to reset velocity here, the movement script will handle that.
		current_hexapod = new_hexapod
	else:
		printerr("Error: hexapod_scene is null. Make sure it's assigned in the inspector.")

func reset() -> void:
	spawn_hexapod() # Best way to reset, use the spawn function.

# Handle environment actions
func _on_environment_handel_action(action_str):
	current_hexapod.handle_action(action_str)

# Handle master actions
func _on_master_handler_handel_action(action_str):
	current_hexapod.handle_action(action_str)
