# Ball Script - Attach to your ball node
extends RigidBody2D

func _ready():
	# Set up physics properties
	linear_damp = 0.5  # Adds some friction
