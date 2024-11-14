extends LineEdit


# Called when the node enters the scene tree for the first time.

func _on_text_changed(new_text):
	var por = int(new_text)
	if por > 65535:
		por = 65535
		text= str(por)
	
