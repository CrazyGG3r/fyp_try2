extends MeshInstance2D
var flag = 0 
func _ready():
	# Generate a random color
	var random_color = Color(randf_range(0,0.15), randf_range(0,0.15), 0)
	modulate = random_color
	
	# Apply the random color to the material
func _process(delta):
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and flag == 0:
			flag = 1
	else:
		flag = 0
	if flag == 1:
		var random_color = Color(randf_range(0.05,0.2), randf_range(0.05,0.2), 0)
		modulate = random_color
