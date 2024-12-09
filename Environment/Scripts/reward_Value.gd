extends RichTextLabel


# Called when the node enters the scene tree for the first time.
func _ready():
	text = str("%.2f"%float(master.reward))


@onready var master = $"../../../Master Handler"
func _process(delta):
	#print(float(master.reward))
	text = str("%.2f"%float(master.reward))
	
