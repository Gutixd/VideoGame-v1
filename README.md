# LÍNEA CERO

**Horror Psicológico 3D — First Person**  
*Godot 4.3 | GDScript | Single Player*

## Concepto

Eres Rodrigo Vásquez, técnico de mantenimiento nocturno del Metro de Santiago. Son las 1:37 AM. Hay una falla de señal entre Baquedano y Santa Lucía. Entrás al túnel con una linterna. Desde ese momento, algo en el metro sabe que estás ahí.

**Duración:** 25–40 minutos por partida  
**Plataforma V1:** Windows .exe / itch.io  
**Setting:** Metro de Santiago, Línea 1 — Estación Baquedano

## Tipo de Miedo: Horror Psicológico Liminal

- ❌ Sin jump scares baratos
- ❌ Sin entidad visible moviéndose
- ❌ Sin gore
- ✅ Dread acumulativo
- ✅ Paranoia visual (cámara inclinada, imágenes sublimales)
- ✅ Sonido como protagonista (80% del miedo es audio)
- ✅ Memoria del lugar (el metro recuerda muertes anteriores)

## Mecánicas V1 (MVP)

| Mecánica | Detalles |
|----------|----------|
| **Linterna con batería** | 180 segundos. Recarga con pilas del escenario. En oscuridad total, la entidad se activa. |
| **Radio de mano** | Única conexión con la superficie. Estática sube cuando la entidad se acerca. |
| **Notas de técnicos** | Lore esparcido en papeles por el escenario. Contradicen lo que el jugador ve. |
| **Sistema de sanidad** | Escala 0–100. Efectos visuales/auditivos según nivel. |
| **Sin combate** | Solo caminar, mirar, interactuar. Si la entidad te alcanza: blackout + respawn. |
| **Una sesión** | Sin guardado automático. 25–40 minutos continuos. Morir tiene consecuencias. |

## Estructura del Nivel

| Zona | Tiempo | Descripción |
|------|--------|-------------|
| **01 — Sala técnica** | 0–5 min | Tutorial implícito. Todo parece rutina. |
| **02 — Andén Baquedano** | 5–15 min | Estación vacía, luces que fallan, panel de llegadas muestra trenes inexistentes. Primer contacto auditivo con la entidad. |
| **03 — Túnel km 1.4** | 15–30 min | Oscuridad total. Entidad activa. Restos del equipo de Rodrigo. Punto de no retorno. |
| **04 — Sala de emergencia** | 30–40 min | Puerta de escape. Su nombre escrito desde adentro, con letra que no es suya. Final abierto. |

## Roadmap V1 (6 semanas)

- **Sem 1:** Setup + Player Controller ← **AQUÍ ESTAMOS**
- **Sem 2:** Blockout del nivel (geometría básica con CSGBox)
- **Sem 3:** Sistema de audio + Sanidad
- **Sem 4:** IA de la entidad (NavigationAgent3D)
- **Sem 5:** Assets y texturas
- **Sem 6:** Lore, polish y export

## Estructura del Proyecto

```
linea_cero/
├── scenes/
│   ├── main.tscn              # escena raíz
│   ├── player.tscn            # FPS controller
│   ├── station_baquedano.tscn # andén principal
│   ├── tunnel.tscn            # tramo de túnel
│   └── entity.tscn            # la entidad
├── scripts/
│   ├── player.gd              # movimiento, linterna, sanity
│   ├── entity_ai.gd           # pathfinding + detección por audio
│   ├── audio_manager.gd       # sistema de sonido 3D
│   ├── sanity_system.gd       # efectos psicológicos
│   └── game_manager.gd        # estado global
├── assets/
│   ├── audio/                 # .ogg: ambience, pasos, estática
│   ├── models/                # .glb: estación, props
│   └── shaders/               # VHS, noise, chromatic aberration
├── project.godot
└── .gitignore
```

## Next Steps

1. ✅ Crear estructura de carpetas
2. ⏳ Crear `player.gd` (FPS controller con linterna)
3. ⏳ Crear escena `main.tscn` con Player
4. ⏳ Crear blockout básico con CSGBox

## Herramientas

- **Motor:** Godot 4.3
- **Scripting:** Claude Code (CLI)
- **3D:** Blender (modelos propios) + Kenney.nl/Sketchfab (props gratuitos)
- **Audio:** Audacity + Freesound.org
- **Texturas:** ambientcg.com
- **Control de versiones:** Git + GitHub
- **Distribución:** itch.io

---

**LÍNEA CERO — GDD V1.0**  
Generado con Claude  
Confidencial — uso interno
