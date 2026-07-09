# CLAUDE.md — LÍNEA CERO

## Proyecto

**LÍNEA CERO** es un juego de horror psicológico 3D first-person hecho en Godot 4.3.

- **Scope:** MVP en 6 semanas
- **Duración:** 25–40 minutos por partida
- **Setting:** Metro de Santiago (Línea 1, Estación Baquedano)
- **Target:** Windows .exe → itch.io

## Arquitectura

### Directorio raíz
```
linea_cero/
├── scenes/        # Escenas .tscn (main, player, level zones, entity)
├── scripts/       # Scripts .gd (player, entity_ai, audio, sanity, game_manager)
├── assets/        # Audio, modelos 3D, shaders
├── project.godot  # Configuración de Godot
└── README.md      # Overview del proyecto
```

### Scripts clave

| Script | Responsabilidad |
|--------|-----------------|
| `player.gd` | FPS controller, linterna, batería, interacción |
| `entity_ai.gd` | IA de la entidad: detección por audio, pathfinding, pasos |
| `sanity_system.gd` | Escala 0–100, efectos visuales/auditivos |
| `audio_manager.gd` | AudioStreamPlayer3D, estática de radio, ambience |
| `game_manager.gd` | Singleton: estado global, persistencia entre muertes |

## Roadmap

**Sem 1 (ACTUAL):** Setup + Player Controller
- ✅ Estructura de carpetas
- ⏳ `player.gd` con CharacterBody3D, Camera3D, linterna
- ⏳ Escena `main.tscn`
- ⏳ Blockout mínimo para testear movimiento

**Sem 2–6:** Ver README.md

## Directrices de desarrollo

### GDScript
- Usar convención snake_case para funciones y variables
- Usar PascalCase para clases
- No comentarios innecesarios (código autoexplicativo)
- Priorizar claridad sobre optimización (es MVP)

### Escenas
- Mantener escenas pequeñas y reutilizables
- Usar instancias en lugar de duplicar nodos
- Nombrar nodos con nombres descriptivos

### Assets
- Audio: .ogg (comprimido, webfriendly)
- Modelos: .glb (GLTF 2.0, lightweight)
- Texturas: PBR (albedo + normal + roughness)

### Pipeline de modelado (obligatorio a partir de And��n Baquedano)
- **Toda la geometría 3D se modela en Blender, nunca con CSG directo en Godot.**
- Cada mapa se genera con un script Python (`bpy`) ejecutado en modo headless: `blender --background --python script.py`
- Cada script de mapa debe producir:
  1. Archivo `.blend` fuente (editable, con colecciones organizadas por categoría: Arquitectura, Props, Iluminación, Señalética)
  2. Exportación `.glb` (GLTF binario) lista para importar en Godot 4 sin retoques
  3. Materiales asignados por submesh, UVs básicos correctos (sin overlaps, sin estiramiento)
  4. Nombres de objetos profesionales y descriptivos (ej. `Columna_Estructural_01`, no `Cube.003`)
  5. Pivotes/orígenes correctos (base del objeto para props que se paran en el piso, centro para elementos suspendidos)
  6. Escala real 1:1 (1 unidad Blender = 1 metro = 1 unidad Godot)
- Ubicación de scripts de generación: `blender_pipeline/<nombre_mapa>/generar_<nombre_mapa>.py`
- Ubicación de salidas: `.blend` en `blender_pipeline/<nombre_mapa>/`, `.glb` final en `assets/models/<nombre_mapa>/`
- Godot solo importa el `.glb` — no se debe editar geometría dentro del editor de Godot

### Control de versiones
- Commits frecuentes (1 feature = 1 commit)
- Mensajes claros: "Add player movement", "Implement sanity system decay"
- No commitear builds, solo source

## Herramientas recomendadas

- **Godot 4.3:** Motor principal
- **Claude Code CLI:** Generar scripts desde terminal
- **Blender:** Modelado 3D
- **Audacity:** Edición de audio
- **Git:** Control de versiones

## Recursos gratuitos

- **3D:** Kenney.nl, Sketchfab (CC0), Blender primitives
- **Texturas:** ambientcg.com, Polyhaven
- **Audio:** Freesound.org, ZapSplat
- **Shaders:** godotshaders.com

## Notas importantes

1. El juego NO tiene guardado automático — toda una sesión es continua
2. La entidad NUNCA es visible (solo se escucha)
3. El 80% del miedo es sonido, no visuals
4. La memoria del lugar (Game Manager) debe persistir entre respawns
5. No hay UI durante gameplay — solo diegético (linterna, radio, carteles)

---

**Generado:** 2026-07-09  
**Versión:** GDD 1.0  
**Estado:** En desarrollo — Sem 1
