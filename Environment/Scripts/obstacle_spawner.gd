extends Node2D

@export var scene_to_spawn: PackedScene

@onready var obs_min: Marker2D = $"../Reset_positions/obs_min"
@onready var obs_max: Marker2D = $"../Reset_positions/obs_max"

var current_obstacle: Node2D = null

func _ready():
	reset()

func reset() -> void:
	call_deferred("spawn_obstacle")

func spawn_obstacle() -> void:
	if current_obstacle:
		current_obstacle.queue_free()
		current_obstacle = null

	if scene_to_spawn != null:
		var new_obstacle = scene_to_spawn.instantiate()
		add_child(new_obstacle)
		current_obstacle = new_obstacle

		var min_pos = obs_min.global_position
		var max_pos = obs_max.global_position

		var rand_x = randf_range(min_pos.x, max_pos.x)
		var rand_y = randf_range(min_pos.y, max_pos.y)
		new_obstacle.global_position = Vector2(rand_x, rand_y)
	else:
		printerr("Error: scene_to_spawn is null. Assign it in the inspector.")
