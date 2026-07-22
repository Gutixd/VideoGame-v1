# 🚇 TREN — Metro (Blender + Godot)

Modelo 3D de un tren de metro (estilo Metro de Santiago, estación San Pablo) con
una demo jugable en Godot: el tren llega al andén, abre las puertas, el jugador
entra y las puertas se cierran.

## Contenido

| Archivo | Descripción |
|---|---|
| `metro.blend` | Escena 3D completa en Blender (tren de 3 coches, estación, interior, cabina) |
| `metro_blender.py` | Script generador — reconstruye toda la escena desde cero en Blender |
| `metro_llegada.gif` | Animación: el tren llegando al andén |
| `metro_cabina.gif` | Recorrido en primera persona entrando a la cabina de conducción |
| `godot_metro/` | Proyecto de Godot 4.7 con la demo jugable |

## El modelo (Blender)

- Tren turquesa de **3 coches** con morro redondeado y parabrisas inclinado
- Carrocería con banda de ventanas, puertas, bogies y ruedas
- Luces de posición rojo/blanco/rojo y faros en el frontal
- **Estación** con andén, línea amarilla de seguridad, vía, túnel y cartel "SAN PABLO"
- **Interior** con asientos naranjos, barras verticales y luces de techo
- **Cabina de conducción**: tablero inclinado, dos pantallas (datos y emergencia),
  velocímetro, dos palancas de mando, botón de emergencia tipo hongo, filas de
  botones de colores, asiento del conductor y mampara con puerta

Para regenerar la escena desde cero: abrir Blender → pestaña **Scripting** →
pegar `metro_blender.py` → **Run Script**.

## La demo (Godot 4.7)

Abrir `godot_metro/project.godot` en Godot y ejecutar.

### Controles

| Tecla | Acción |
|---|---|
| `WASD` | Moverte |
| `Mouse` | Mirar |
| `R` | Reiniciar la escena |
| `ESC` | Liberar el cursor |

### Secuencia

1. El tren llega desde el túnel y frena progresivamente en el andén
2. Se abren las puertas del lado del andén (18 hojas: paneles + vidrios)
3. Caminas hacia el tren y entras por la puerta del coche del medio
4. Un `Area3D` detecta tu entrada y **las puertas se cierran** tras 1 segundo

### Estructura del proyecto

- `game.gd` — llegada del tren, apertura/cierre de puertas, detección de entrada
- `player.gd` — controlador en primera persona
- `models/metro.glb` — modelo exportado desde Blender
- `models/doors.json` — posiciones de las puertas del lado del andén

## Notas técnicas

- El `.glb` se exporta desde Blender con los modificadores aplicados y el tren en
  reposo; el movimiento lo controla Godot por código.
- Al exportar se añaden planos oscuros ("vanos") detrás de cada puerta del lado
  del andén, para que al abrirse se vea un hueco y no la carrocería.
- El tren **no tiene colisión en las paredes** (solo el piso), para que nada
  bloquee la entrada del jugador.
