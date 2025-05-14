extends Node2D

var max_offset = 10.0
var eyes = []
#@onready var ball_spawner: Node2D = $"../../Ball_Spawner"
var ball_spawner = null
func _ready():
	ball_spawner = get_parent().get_parent().ball_spawn
	var children = get_children()
	for i in range(0, children.size(), 2):
		if i + 1 >= children.size():
			break
		var white = children[i]
		var pupil = children[i + 1]
		if white is MeshInstance2D and pupil is MeshInstance2D:
			var sclera_radius = white.scale.x
			var pupil_radius = pupil.scale.x
			eyes.append({
				"white": white,
				"pupil": pupil,
				"sclera_radius": sclera_radius,
				"pupil_radius": pupil_radius
			})

func _process(delta):
	for eye in eyes:
		var white = eye.white
		var pupil = eye.pupil
		var r = eye.sclera_radius - eye.pupil_radius - eye.sclera_radius/max_offset

		var dir = ball_spawner.current_ball.global_position - white.global_position
		if dir.length() > r:
			dir = dir.normalized() * r
		pupil.global_position = white.global_position + dir
