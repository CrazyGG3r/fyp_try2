extends LineEdit

func _ready():
	max_length = 15  # Max length for "xxx.xxx.xxx.xxx"

func _on_text_changed(new_text):
	print(new_text)
	caret_column = new_text.length()  # Keep cursor at the end
