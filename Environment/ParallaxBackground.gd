extends ParallaxBackground

@export var scroll_speed: Vector2 = Vector2(20, 0) # Adjust speed as needed

func _process(delta):
	scroll_offset += scroll_speed * delta
