# LÉEME — Metro Baquedano H (beta)

Guía rápida para abrir y ejecutar el mapa **Metro Baquedano H** en Blender y luego en Godot.

## Requisitos

- **Godot 4.7** (stable) — https://godotengine.org/download
- **Blender** (4.x o 5.x) instalado — necesario para que Godot importe el modelo `.blend`.

## 1) Clonar el repo

```bash
git clone https://github.com/Gutixd/VideoGame-v1.git
cd VideoGame-v1
```

## 2) Editar el mapa en Blender

El modelo que usa la escena es **este** (¡no las otras copias del proyecto!):

```
blender_pipeline/METRO_BAQUEDANO_H/Metro_Baquedano_H.blend
```

Ábrelo en Blender, ajusta lo que necesites y **guarda con `Ctrl+S`** en ese mismo archivo.

> Diseño / referencia del mapa: `design_docs/Metro_Baquedano_H.md`

## 3) Abrir y ejecutar en Godot

1. Abre Godot 4.7 → **Import** → selecciona el `project.godot` de la carpeta clonada.
2. **La primera vez**, Godot reimporta el `.blend`. Para eso necesita saber dónde está Blender:
   - `Editor` → `Editor Settings` → `FileSystem` → `Import` → `Blender`
   - Activa **Blender 3 Path** y apunta a la carpeta de tu instalación de Blender
	 (ej. `C:\Program Files\Blender Foundation\Blender 5.1`). Reinicia Godot si lo pide.
3. En el panel *FileSystem*, abre la escena:
   ```
   scenes/metro_baquedano_h.tscn
   ```
4. Pulsa **F6** (Ejecutar escena actual) para probar el mapa.
   - Controles: **WASD** moverse, **ratón** mirar (first-person).

## 4) Ciclo de iteración Blender ↔ Godot

1. Editas el `.blend` en Blender → **Ctrl+S**.
2. Con el editor de Godot abierto, **reimporta solo** el modelo automáticamente.
3. Vuelve a pulsar **F6** en Godot para ver los cambios.

## Notas

- Si al abrir el proyecto Godot muestra un aviso sobre el addon **`godot_ai`**, ignóralo:
  es una herramienta de desarrollo local (no se sube al repo) y Godot la desactiva sola.
  El mapa funciona sin ella.
- La caché de importación (`.godot/`) no está en el repo: se regenera sola al abrir el proyecto.
