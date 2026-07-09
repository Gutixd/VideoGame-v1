extends StaticBody3D

const TEXTO_NOTA := """NOTA DE MANTENIMIENTO - TURNO NOCHE

Si estás leyendo esto, ya escuchaste los pasos.
No corras la radio de canal. No sirve.
Rodrigo dijo que iba a revisar el panel de la
via 1 y no volvió a la sala técnica.

- J.M."""

var leida := false

func interact() -> void:
	leida = true
	print("[Nota encontrada] ", TEXTO_NOTA)
