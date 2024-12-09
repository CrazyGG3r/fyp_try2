extends RichTextLabel


# Called when the node enters the scene tree for the first time.
func _ready():
	text = 	str("%.2f"%(float(timee.time_left)+1.0))


@onready var timee = $"../episode_Timer"
func _process(delta):
	text = 	str("%.2f"%(float(timee.time_left)))
