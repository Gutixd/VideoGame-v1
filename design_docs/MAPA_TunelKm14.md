# MAPA_TunelKm14.md

**Proyecto:** LÍNEA CERO
**Zona:** 03 — Túnel km 1.4 y Zona 04 — Sala de Emergencia
**Autor:** Senior Level Designer / Environment Artist
**Estado:** En desarrollo
**Versión:** 1.0

---

## 1. Información general

| Campo | Valor |
|---|---|
| Nombre | Túnel km 1.4 y Sala de Emergencia |
| Zona (GDD) | 03 y 04 |
| Objetivo narrativo | Transición a oscuridad total, opresión. El jugador sabe que ya no está a salvo. La tensión culmina con la Sala de Emergencia y su revelación final. |
| Objetivo del jugador | Atravesar el túnel a oscuras esquivando (o huyendo de) la entidad, encontrar los restos del equipo y llegar a la puerta de escape. |
| Duración estimada | 15–20 min |
| Nivel de tensión | Alto → Muy Alto (Pico del juego). Oscuridad, persecución, paranoia. |
| Inspiración | Silent Hill (transiciones a "Otherworld"), Metro 2033 (túneles opresivos y anomalías). |

---

## 2. Medidas

| Elemento | Medida usada en el nivel | Justificación |
|---|---|---|
| Largo total del túnel | 120 m | Suficientemente largo para sentir desesperación, permite encuentros dinámicos. |
| Ancho del túnel | 4.5 m | Apenas más ancho que un tren, claustrofóbico. |
| Alto en clave de bóveda | 4.5 m | Bóveda de medio punto estándar para túnel de vía simple. |
| Nichos de refugio | Cada 30 m | Pequeños huecos en la pared donde el jugador puede apagar la luz y esconderse. |
| Sala de Emergencia | 5x5 m | Habitación estrecha al final del recorrido. |

---

## 3. Descripción Visual y Gameplay

El jugador desciende desde el andén de Baquedano hacia las vías. Una vez abajo, no hay vuelta atrás (el borde del andén es muy alto para subir). 
El túnel es de un solo carril (vía este u oeste, dependiendo de dónde bajó). La oscuridad es casi absoluta. La linterna es esencial, pero su luz atrae a la entidad.
- **Nichos:** Huecos (1x1m) en los muros laterales. Si la entidad se acerca, el jugador debe meterse en un nicho, apagar la linterna y no moverse.
- **Restos:** A los 60m se encuentra una mochila con baterías y una nota escalofriante ("Ella nos oye cuando encendemos la luz").
- **Sala de Emergencia:** Al final de los 120m, una luz roja intermitente marca una puerta metálica pesada en un costado del túnel. Al entrar, la puerta se cierra sola. 

---

## 4. IA de la Entidad

La entidad (`entity_ai.gd`) usa `NavigationAgent3D` y un sistema de sentidos (Oído y Vista).
- **Vista (Luz):** Si el jugador tiene la linterna encendida y está en línea de visión, la entidad lo detecta rápidamente.
- **Oído (Pasos):** Si el jugador corre (sprint, aunque el juego base solo tiene un walk lento, el ruido de los pies alerta).
- **Comportamiento:** Si detecta al jugador, inicia persecución (sonidos distorsionados crecientes). Si el jugador apaga la luz y se esconde en un nicho, la entidad perderá el rastro tras unos segundos y volverá a patrullar el túnel. Si atrapa al jugador, fundido a negro y reinicio en el Andén.

---

## 5. Assets (Blender)
- Túnel modular de 10m (recto).
- Muro con nicho de refugio.
- Durmientes, balasto y rieles.
- Puerta pesada de Sala de Emergencia.
- Interior de Sala de Emergencia (paredes de concreto, tablero eléctrico, nombre rayado).
