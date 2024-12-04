extends Node2D

var num_balls = 1
var ball_scene = preload("res://Scenes/ball.tscn")  # Replace with the path to your ball scene
var balls = []  # Array to store references to the balls
func _ready():
	generate_random_balls(num_balls)

func generate_random_balls(count: int):
	for i in range(count):
		var ball_instance = ball_scene.instantiate()
		var random_position = Vector2(0,0)
		ball_instance.position = random_position
		add_child(ball_instance)
		balls.append(ball_instance)  # Store reference in the array

# Accessing the position of a specific ball
func _process(delta):
	pass
