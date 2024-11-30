extends Node2D

# Set the number of balls you want to generate
var num_balls = 10
var ball_scene = preload("res://Scenes/ball.tscn")  # Replace with the path to your ball scene

func _ready():
	generate_random_balls(num_balls)

# Function to generate random balls
func generate_random_balls(count: int):
	for i in range(count):
		# Create an instance of the ball scene
		var ball_instance = ball_scene.instantiate()
		
		# Set a random position within a defined range (you can adjust the range as needed)
		var random_position = Vector2(randf_range(-200, 200), randf_range(-200, 200))  # Example range: -200 to 200
		
		# Set the ball's position
		ball_instance.position = random_position
		
		# Add the ball to the scene
		add_child(ball_instance)
