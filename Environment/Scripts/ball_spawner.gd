extends Node2D

@export var ball_scene:PackedScene
@onready var ball_reset: Marker2D = $"../Reset_positions/Ball"

var current_ball: RigidBody2D = null
func _ready() -> void:
	spawn_ball()

func reset():
	call_deferred("spawn_ball")


func spawn_ball() -> void:
	if current_ball:
		current_ball.queue_free()
		current_ball = null# Optional: or hide/disable if you want to reuse
	var new_ball = ball_scene.instantiate()
	new_ball.global_position = ball_reset.global_position
	add_child(new_ball) #add the new ball to the scene.
	new_ball.linear_velocity = Vector2.ZERO
	new_ball.angular_velocity = 0
	current_ball = new_ball # Update the current_ball reference.
