extends RigidBody2D


# Called when the node enters the scene tree for the first time.
@onready var start_pos = $"../Reset_positions/Ball"
var ball_scene = preload("res://Scenes/ball.tscn")
var ball: RigidBody2D

func _ready():
	load_ball()
	
func unload_ball():
	if ball:
		ball.queue_free()
		ball = null
func load_ball():
	ball = ball_scene.instantiate()
	add_child(ball)
	ball.global_position = start_pos.global_position  # Set the initial position of the ball
func reset():
	unload_ball()
	load_ball()
func _process(delta):
	pass
