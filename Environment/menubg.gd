extends MeshInstance2D

func _ready():
	# Generate a random color
	var random_color = Color(randf_range(0,0.2), randf_range(0,0.2), 0)
	modulate = random_color
	
	# Apply the random color to the material
func _process(delta):
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		var random_color = Color(randf_range(0,0.2), randf_range(0,0.2), 0)
		modulate = random_color
