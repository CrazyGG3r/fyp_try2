extends CharacterBody2D

@export var speed = 200  # Pixels per second

func _ready():
	pass

func _process(delta):
	var velocity = Vector2.ZERO
	
	if Input.is_action_pressed("ui_right"):
		velocity.x += 1
	if Input.is_action_pressed("ui_left"):
		velocity.x -= 1
	if Input.is_action_pressed("ui_down"):
		velocity.y += 1
	if Input.is_action_pressed("ui_up"):
		velocity.y -= 1
	
	# Normalize the velocity to ensure consistent speed in all directions
	if velocity.length() > 0:
		velocity = velocity.normalized() * speed
	
	# Move the node
	position += velocity * delta
