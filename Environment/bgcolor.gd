extends MeshInstance2D
#
@export var Color_bright = Color(randf_range(0.3,0.8),randf_range(0.3,0.8),randf_range(0.3,0.8))#bright
@export var Color_Dark = Color(randf_range(0.02,0.2),randf_range(0.02,0.2),randf_range(0.02,0.2))#dark
@export var colors = []

func _ready():
	#var color_A = Color(100/255.0, 100/255.0, 100/255.0)
	#Color_bright = Color(randf_range(0.3,0.8),randf_range(0.3,0.8),randf_range(0.3,0.8))#bright
	#Color_Dark = Color(randf_range(0.02,0.2),randf_range(0.02,0.2),randf_range(0.02,0.2))#dark
	Color_bright = Color(0.6,0.42,0.43)
	Color_Dark = Color(0.19,0.0,0.0)
	modulate = Color_Dark
	var color_B = Color_bright
	var color_A = Color_Dark
	#var color_B = Color(10/255.0, 10/255.0, 10/255.0)
# Number of steps
	var steps = 12
	
	for i in range(steps):
		var t = i / float(steps - 1)  # Interpolation factor (from 0 to 1)
		var interpolated_color = color_A.lerp(color_B, t)
		colors.append(interpolated_color)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
		

	
