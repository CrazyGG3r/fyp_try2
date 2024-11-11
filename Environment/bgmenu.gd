extends ParallaxBackground


@export var master_scale = 1
@export var master_opacity = 1

#@onready var L1 = $L1
#@onready var L2 = $L2
#@onready var L3 = $L3
#@onready var L4 = $L4
#@onready var L5 = $L5
#@onready var L6 = $L6
#
#@onready var L1s = $L1/L2Bg
#@onready var L2s = $L2/L2Bg
#@onready var L3s = $L3/L2Bg
#@onready var L4s = $L4/L2Bg
#@onready var L5s = $L5/L2Bg
#@onready var L6s = $L6/L2Bg
# Called when the node enters the scene tree for the first time.
@onready var Llist = [$L1,$L7,$L2,$L8,$L3,$L9,$L4,$L10,$L5,$L11,$L6,$L12]
@onready var Lslist = 	[$L1/L2Bg,$L7/L2Bg,$L2/L2Bg,$L8/L2Bg,$L3/L2Bg,$L9/L2Bg,
						$L4/L2Bg,$L10/L2Bg,$L5/L2Bg,$L11/L2Bg,$L6/L2Bg,$L12/L2Bg]
@onready var bg_ = $bgcolor
@onready var factor = 1.0/6.0
@export var spacing = 8

func _ready():
	
	for n in range(Llist.size()):
		var Layerr = Llist[n]
		var Layerr_sprite = Lslist[n]
		#factor = factor * (n + 1)
		#Layerr_sprite.position.x = $L1/L2Bg.position.y + (n * spacing)
		Layerr.motion_scale.x = master_scale * factor * float(n)
		Layerr.motion_scale.y = master_scale * factor * float(n)
		#Layerr_sprite.modulate.a = master_opacity * factor * float(n+1.0)
		Layerr_sprite.modulate = bg_.colors[n+1]
		
		
		
#def all layers

# Called every frame. 'delta' is the elapsed time since the previous frame.
@export var speed = 20
func _process(delta):
	scroll_offset.x -= speed * delta


func _on_bgcolor_visibility_changed():
	_ready()


func _on_bgcolor_item_rect_changed():
	pass # Replace with function body.

func _on_bgcolor_colo_change():
	_ready()
func _on_bgcolor_texture_changed():
	_ready()
