extends RichTextLabel

@onready var master = $"../../../Master Handler"
# Called when the node enters the scene tree for the first time.
func _ready():
	text = str(master.episode_num)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	text = str(master.episode_num)
