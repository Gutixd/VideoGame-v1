extends StaticBody3D

const TEXTO_NOTA := """REGISTRO DE SEGURIDAD - PLAZA DE MAIPÚ - 01:14 AM

La explanada de la superficie está cerrada y bloqueada desde la medianoche, pero los sensores de movimiento en el andén central siguen registrando actividad.
He bajado a revisar tres veces. La estación está completamente vacía. Solo se escucha el zumbido de los transformadores en la boletería.
Sin embargo, las cámaras del túnel de cola de maniobras no paran de captar estática intermitente. 
Si llegas a escuchar el silbato de un tren acercándose desde las vías oscuras, NO te asomes al borde del andén.

- Guardia Nocturno"""

var leida := false

func interact() -> void:
	leida = true
	print("[Nota encontrada en Plaza de Maipú] \n", TEXTO_NOTA)
