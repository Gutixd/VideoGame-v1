extends AudioStreamPlayer

func _ready() -> void:
	if stream and stream is AudioStreamWAV:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	volume_db = -12.0
	play()
