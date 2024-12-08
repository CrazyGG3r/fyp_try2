extends RichTextLabel


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


@onready var timee = $"../episode_Timer"
func _process(delta):
	text = 	str(int(timee.time_left)+1)
