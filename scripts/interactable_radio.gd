extends StaticBody3D

var activa := false

func interact() -> void:
	activa = not activa
	var audio = get_node_or_null("../../Audio/RadioEstaticaPlayer")
	if audio:
		if activa:
			audio.play()
		else:
			audio.stop()
	print("[Radio] ", "Estática activada" if activa else "Radio apagada")
