# MAPA_HallCombinacionL5.md

**Proyecto:** LÍNEA CERO
**Zona:** 01B — Hall de Combinación Baquedano (L1 ↔ L5)
**Autor:** Senior Level Designer / Environment Artist (documento de diseño)
**Estado:** 🟡 Pendiente de aprobación — NO IMPLEMENTAR hasta visto bueno
**Versión:** 1.0

---

## 0. Fuente de investigación (Fase 1)

Basado en fuentes **verificadas** (no estimación por analogía), recopiladas y catalogadas en [`referencias_fotograficas/README.md`](../referencias_fotograficas/README.md):

- **Metro de Santiago, página oficial** (metro.cl/el-viaje/estaciones/BA y metro.cl/estacion/BQ)
- **Wikipedia ES**, artículo verificado de Baquedano (estación)
- **Wikimedia Commons**, categoría "Baquedano station" (102 archivos catalogados)

**Hallazgos clave que definen esta zona:**

| Aspecto | Dato | Confianza |
|---|---|---|
| Configuración | Estación de combinación L1 ↔ L5, **6 niveles totales** | Alta — fuente oficial + Wikipedia |
| Andenes/vías | 6 en total, **solo 4 operativos** (2 de L1, 2 de L5) — **2 reservados para la futura Línea 7** | Alta |
| Profundidad | L1 (1977, tajo abierto/cut-and-cover) y L5 (1997, excavación subterránea profunda) están a **profundidades distintas** | Alta |
| Nivel de combinación | Existe un nivel dedicado de transferencia, con ~200+ m² de muro ocupados por arte (MetroArte) | Alta |
| Accesos | 4 accesos de superficie (A–D), uno con ascensor | Alta |
| Ascensores | 4 totales: 1 de acceso + 3 de transferencia interna L1↔L5 | Alta |
| Servicios reales | Máquinas Bip!, oficina de atención, cajero, tienda Maxi-K, Bibliometro (biblioteca), murales "La Bajada", "El Santiaguillo", "Ágora" (400 m², sobre escaleras de acceso al andén) | Alta |
| Sistema eléctrico | 750V DC por riel guía (tercer riel), no catenaria aérea | Alta |
| Historia reciente | Incendio en acceso principal el 25-oct-2019 (protestas); reconstrucción completa terminada 9-ene-2024, sin la antigua "plaza hundida" | Alta |
| Perfil arquitectónico de L5 | **No documentado con certeza** — pero al ser excavación subterránea profunda de 1997 (vs. tajo abierto de 1977 para L1), es consistente con perfil de túnel circular/tuneladora, arquitectura más moderna que la bóveda de cañón de L1 | **[ESTIMADO]**, decisión de diseño justificada abajo |
| Dimensiones de hall, escaleras, ancho de pasillos | Sin plano público con medidas exactas encontrado (el PDF isométrico de metro.cl referenciado en búsquedas retornó 404) | **[ESTIMADO]**, ver sección 2 |

**Decisión de diseño clave:** dado que L1 (bóveda de hormigón, cerámica crema/ocre, estética 1975) y L5 (excavación moderna 1997) son constructivamente distintas, **el andén de Línea 5 debe verse arquitectónicamente diferente al de Línea 1** ya construido — perfil de túnel más cilíndrico, materiales más modernos (paneles, acero, iluminación empotrada en vez de cornisa clásica). Esto no es solo fidelidad histórica: el contraste visual entre "L1 clásica" y "L5 moderna" es una herramienta de horror liminal — cruzar de una arquitectura a otra marca un quiebre perceptual para el jugador.

---

## 1. Información general

| Campo | Valor |
|---|---|
| Nombre | Hall de Combinación Baquedano (L1 ↔ L5) |
| Zona (GDD, insertada) | 01B — entre Sala Técnica (01) y Andén Baquedano L1 (02), sin renumerar el GDD general |
| Objetivo narrativo | Establecer la escala real multi-nivel de la estación antes de llegar al andén L1. Plantar el primer indicio de anomalía: la Línea 5 y las plataformas reservadas para L7 deberían estar cerradas de noche, pero algo las mantiene accesibles |
| Objetivo del jugador | Cruzar el hall desde el acceso de mantenimiento, bajar por las escaleras de combinación, llegar al andén L1 (zona 02 ya construida) |
| Duración estimada | 3–6 min (zona de tránsito breve, no debe inflar el ritmo total de 25–40 min del GDD) |
| Nivel de tensión | Muy bajo — más calmo aún que el andén. Es la "normalidad" más profunda antes de que empiece a fallar |
| Inspiración | Mismas del GDD general, con énfasis adicional en el hall de estación real vacía de noche (fotografía de Wikimedia Commons de "Baquedano nivel de combinación L1 y L5.jpg" como referencia directa) |

---

## 2. Medidas

| Elemento | Medida real | Medida usada en el nivel | Justificación |
|---|---|---|---|
| Hall de combinación (ancho × largo) | Sin plano público exacto | **20 × 25 m** [ESTIMADO] | Basado en la superficie de arte mural confirmada (~200+ m²) más circulación y torniquetes; genera un hall que se siente "grande" comparado con el andón de 7m de ancho, reforzando escala institucional |
| Alto de hall | Sin dato público | **4.5 m** [ESTIMADO] | Más alto que el andén (4.3 m arranque) porque es zona de circulación con mezzanine parcial, consistente con estaciones de combinación reales de la época |
| Diferencia de profundidad L1↔L5 | Sin dato público, pero confirmado que existe (construcciones de 1977 y 1997 respectivamente) | **10 m** [ESTIMADO] | Suficiente para justificar 2 tramos de escalera mecánica + descansos, consistente con "numerosas escaleras" mencionado en fuentes |
| Ancho de andén L5 | Sin dato específico | **7 m** (igual que L1) | Sin evidencia de que difiera; se mantiene igual por consistencia funcional del sistema |
| Alto de andén L5 (perfil moderno) | Sin dato específico | **4.0 m** techo plano/panelado [ESTIMADO, ver decisión de diseño en sección 0] | Perfil de túnel excavado moderno, más bajo y regular que la bóveda de L1, con cielo falso panelado en vez de hormigón visto |
| Largo de andén L5 modelado | — | **60 m** [decisión de alcance, ver sección 15] | Menor que los 100 m de L1: esta zona es de tránsito/atmósfera, no requiere la escala completa del andén principal donde ocurre el gameplay central |
| Escala real | 1 unidad Godot = 1 metro | — | Estándar del proyecto |

---

## 3. Plano superior (planta técnica)

Vista en planta. El jugador entra por el Norte (desde Sala Técnica, vía un pasillo de mantenimiento no documentado en detalle — ver sección 15), cruza el hall, y desciende por las escaleras de combinación hacia el Sur, donde se conecta con el Andén Baquedano L1 ya construido (entra exactamente en el punto donde hoy está `Reja_Escalera_Norte`, que en esta ampliación deja de ser un cierre y pasa a ser una puerta funcional).

```
NORTE (entrada desde pasillo de mantenimiento / Sala Técnica)
│
│   ┌───────────────────────────────────────────────────────────┐
│   │ 01                                                    02  │  ← Acceso de mantenimiento + Acceso público sellado (referencia a Accesos A-D reales)
│   ├───────────────────────────────────────────────────────────┤
│   │                                                            │
│   │  03        04         05                    06            │
│   │ (torni-  (bole-    (Bibliometro           (Maxi-K,        │  ← HALL DE COMBINACIÓN (zona jugable, 20×25m)
│   │ quetes)  tería)     / cajero)              vacío)         │
│   │                                                            │
│   │              07 (mural "Ágora" — pared este, 400m² real)  │
│   ├───────────────────────────────────────────────────────────┤
│   │ 08  Escalera mecánica + fija, tramo 1 (hacia L1)          │
│   ├───────────────────────────────────────────────────────────┤
│   │ 09  Descanso intermedio                                   │
│   ├───────────────────────────────────────────────────────────┤
│   │ 10  Escalera mecánica + fija, tramo 2 (hacia L1)          │
│   └───────────────────────┬───────────────────────┬───────────┘
│                            │                       │
│                    11 (hacia Andén L1,       12 (hacia Andén L5,
│                     zona 02 ya construida)    esta zona, ver abajo)
│
SUR (Andén L1 — conecta con zona ya construida)


Rama lateral (Línea 5, mismo nivel de hall, acceso independiente):

│   ┌───────────────────────────────────────────────────────────┐
│   │ 13  Boca de acceso a And��n L5 (moderno, perfil distinto) │
│   ├───────────────────────────────────────────────────────────┤
│   │░░░░░░░░░░░░░░░░░ VÍA L5 (foso, no transitable) ░░░░░░░░░░│
│   ├──┬──────────────────────────────────────────────────┬──┬──┤
│   │14│  ANDÉN L5 (60m, perfil moderno panelado)          │14│15│
│   ├──┴──────────────────────────────────────────────────┴──┼──┤
│   │░░░░░░░░░░░░░░░░░ VÍA L5 (foso, no transitable) ░░░░░░░░░░│
│   ├───────────────────────────────────────────────────────────┤
│   │ 16  Reja "PLATAFORMA RESERVADA — LÍNEA 7" (clausurada,   │
│   │     visible pero inaccesible — horror liminal)            │
│   └───────────────────────────────────────────────────────────┘
```

### Leyenda numerada

| # | Elemento | Descripción funcional |
|---|---|---|
| 01 | Acceso de mantenimiento (entrada del jugador) | Conecta con el pasillo que viene de Sala Técnica. Puerta de servicio, sin señalética pública |
| 02 | Acceso público sellado | Representa uno de los 4 accesos reales (A–D) de superficie; aparece cerrado con reja "FUERA DE SERVICIO — HORARIO NOCTURNO", refuerza que el jugador está donde no debería |
| 03 | Torniquetes (fila de 4-5) | Función real confirmada. Todos abiertos/sin energía — otra pista de anomalía (de noche deberían estar bloqueados) |
| 04 | Boletería / oficina de atención | Basada en servicio real confirmado (oficina de atención al cliente) |
| 05 | Bibliometro + cajero automático | Servicios reales confirmados. La Bibliometro (biblioteca) es un detalle único de Baquedano — gran oportunidad de prop narrativo (libro abandonado, ficha de préstamo) |
| 06 | Local comercial vacío (ex Maxi-K) | Servicio real confirmado, representado cerrado/vacío por la hora |
| 07 | Muro con mural "Ágora" (referencia real) | El mural real de Javier Godoy (400 m², fotografías b/n de manifestaciones 1998-2016) — reproducir como textura de decal, no modelado 3D detallado. Fuerte valor atmosférico: rostros de multitudes en un hall vacío |
| 08, 10 | Escaleras mecánica + fija, dos tramos | Confirma "numerosas escaleras mecánicas y estándar" de las fuentes. Detenidas/sin energía (mecánica apagada, el jugador camina sobre los escalones) |
| 09 | Descanso intermedio entre tramos | Compensa la diferencia de profundidad estimada de 10m entre hall y andenes |
| 11 | Conexión hacia Andén L1 (zona 02 ya construida) | Este es el punto de unión real con `Reja_Escalera_Norte` del documento existente — en la implementación, esa reja se reemplaza por un pasaje abierto |
| 12 | Bifurcación hacia Andén L5 | Pasillo corto que lleva a la rama lateral L5 |
| 13 | Boca de acceso a andén L5 | Transición arquitectónica: el jugador nota el cambio de material/perfil al entrar (bóveda clásica → túnel moderno panelado) |
| 14 | Barreras de extremo del andén L5 | Igual función que las del andén L1 |
| 15 | Extremo sur del andén L5 | Sin punto de descenso a vía en esta zona — a diferencia de L1, aquí el jugador NO puede bajar a los rieles (el descenso narrativo real ocurre en la zona L1 ya construida) |
| 16 | Reja de plataforma reservada (Línea 7) | Elemento real confirmado (2 andenes reservados sin operar). Visible a través de una reja o vidrio sucio al fondo del andén L5, completamente oscura, sin luces — el mayor "espacio liminal" de esta zona: una plataforma que nunca ha tenido trenes |

---

## 4. Vista isométrica (descripción)

El hall se percibe como un volumen **más ancho y más iluminado** que cualquier zona anterior del juego — contraste deliberado: después de la Sala Técnica (pequeña, íntima) y antes del Andén L1 (largo pero estrecho), el Hall es la única zona con sensación de "espacio abierto público". Esto hace que su vacío se sienta más antinatural: un lugar diseñado para multitudes, completamente solo.

- **Volumen dominante:** techo plano a 4.5m con iluminación empotrada en línea recta (no la cornisa curva de la Sala Técnica ni del Andén), transmitiendo una estética más "oficina institucional" que "túnel".
- **Punto focal:** el mural "Ágora" en la pared este — filas de rostros fotografiados en blanco y negro, observando al jugador cruzar el hall vacío. No se anima ni cobra vida (nunca hay elementos sobrenaturales visibles, según GDD), pero su sola presencia estática genera la sensación de ser observado.
- **Ramificación:** desde el hall, el jugador ve claramente 3 caminos: escaleras hacia L1 (su objetivo), acceso a L5 (opcional, explorable), acceso público sellado (bloqueado, refuerza linealidad).
- **Contraste arquitectónico L1 vs L5:** al asomarse al andén L5 desde el punto 13, el jugador nota el cambio de bóveda de hormigón visto a un cielo panelado más bajo y uniforme — sutil pero perceptible, sin necesidad de texto explicativo.
- **Recorrido:** Norte→Sur con una bifurcación opcional (L5) antes de la conexión obligatoria hacia el Andén L1. El andén L5 es un callejón sin salida narrativo (el jugador debe volver al hall para continuar), usado para densidad atmosférica, no para progreso.

---

## 5. Blockout (solo cajas — sin detalle)

Origen local de esta zona: (0,0,0) = centro del hall a nivel de piso. Eje +Z hacia el Sur (hacia Andén L1), eje +X hacia el Este. Al integrar con la zona existente, el punto de conexión sur (elemento 11) se alinea con la posición mundial actual de `Reja_Escalera_Norte` del Andén Baquedano.

| Nombre | Tipo de caja | Posición (X,Y,Z) | Escala (Ancho×Alto×Largo) | Función |
|---|---|---|---|---|
| BLOCK_Piso_Hall | Box | (0, 0, 0) | 20 × 0.2 × 25 | Piso del hall |
| BLOCK_Techo_Hall | Box | (0, 4.5, 0) | 20 × 0.2 × 25 | Techo plano (no bóveda) |
| BLOCK_Muro_Norte_Hall | Box | (0, 2.25, -12.5) | 20 × 4.5 × 0.5 | Cierre norte, con hueco para acceso de mantenimiento (01) |
| BLOCK_Muro_Sur_Hall | Box | (0, 2.25, 12.5) | 20 × 4.5 × 0.5 | Cierre sur, con huecos hacia escaleras (08) y bifurcación L5 (12) |
| BLOCK_Muro_Este_Hall | Box | (10, 2.25, 0) | 0.5 × 4.5 × 25 | Muro este (aloja mural Ágora, elemento 07) |
| BLOCK_Muro_Oeste_Hall | Box | (-10, 2.25, 0) | 0.5 × 4.5 × 25 | Muro oeste (aloja acceso público sellado, elemento 02) |
| BLOCK_Torniquetes | Box (×5) | X = -6,-3,0,3,6; Y=0.5; Z=-5 | 0.4 × 1.0 × 0.6 c/u | Fila de torniquetes (elemento 03) |
| BLOCK_Boleteria | Box | (-8, 1.1, -3) | 2.5 × 2.2 × 2 | Volumen de la oficina de atención (04) |
| BLOCK_Bibliometro | Box | (7, 1.1, -3) | 2.5 × 2.2 × 2 | Volumen de biblioteca/cajero (05) |
| BLOCK_Local_Comercial | Box | (7, 1.1, 3) | 2.5 × 2.2 × 2 | Volumen local comercial vacío (06) |
| BLOCK_Escalera_Tramo1 | Box (rampa) | (0, 2.5, 15) | 4 × 5 × 6 | Primer tramo de escalera hacia L1 (08) |
| BLOCK_Descanso | Box | (0, 5, 19) | 4 × 0.2 × 3 | Descanso intermedio (09) |
| BLOCK_Escalera_Tramo2 | Box (rampa) | (0, 7.5, 23) | 4 × 5 × 6 | Segundo tramo hacia L1 (10) |
| BLOCK_Pasillo_L5 | Box | (12, 0, 0) | 4 × 4 × 8 | Pasillo corto de bifurcación hacia L5 (12→13) |
| BLOCK_Piso_AndenL5 | Box | (12, -10, 20) | 7 × 0.2 × 60 | Piso del andén L5 (a -10m de profundidad relativa al hall) |
| BLOCK_Techo_AndenL5 | Box | (12, -6, 20) | 14 × 0.2 × 60 | Techo plano/panelado de L5 (perfil moderno) |
| BLOCK_Reja_PlataformaL7 | Box | (12, -8, 48) | 3.5 × 3 × 0.1 | Reja/vidrio hacia plataforma reservada L7 (16) |

**Nota de blockout:** igual que en el Andén Baquedano, esta fase debe validarse con colisión física real caminando antes de aprobar el paso a Materiales — la lección de la sección 16 del documento del Andén (muro mal alineado con el punto de descenso) aplica aquí también, especialmente en la unión de las escaleras con las diferencias de profundidad.

---

## 6. Lista completa de Assets

### Arquitectura
- Losa de piso de hall (distinta a la del andén — más pulida, estilo "zona pública")
- Muros de hall (lisos, sin bóveda)
- Techo plano panelado con luminarias lineales empotradas
- Escaleras mecánicas (2 tramos) + escalera fija paralela
- Descanso intermedio con baranda
- Torniquetes (modelo genérico, 5 unidades)
- Muro/perfil de andén L5 (arquitectura moderna, distinta a L1)
- Reja/vidrio de plataforma reservada L7

### Props
- Mostrador de boletería
- Estantería y mostrador de Bibliometro
- Cajero automático
- Vitrina de local comercial (vacía, ex Maxi-K)
- Máquinas de carga Bip! (2-3 unidades)
- Papelera/basurero (estilo hall, distinto al del andén)
- Extintor de hall

### Señalética
- Mural "Ágora" (decal de textura, pared este)
- Señalética de accesos A-D (placas)
- Letrero "FUERA DE SERVICIO — HORARIO NOCTURNO" (acceso público sellado)
- Letrero "PLATAFORMA RESERVADA — LÍNEA 7" (reja del fondo del andén L5)
- Mapa de red Metro de Santiago (prop de pared, genérico)
- Flechas direccionales hacia "Línea 1" / "Línea 5"

### Iluminación (objetos físicos)
- Luminaria lineal empotrada de techo (hall, distinta a la cornisa del andén)
- Luminaria de andén L5 (empotrada en panel, más fría/moderna)
- Luz de emergencia (mismo modelo reutilizado del andén L1, consistencia)

### Cableado / Equipos eléctricos
- Tablero eléctrico de hall
- Cableado visible sobre torniquetes

---

## 7. Materiales

| Objeto | Color | Material | Reutilización / Fuente | Roughness | Metallic |
|---|---|---|---|---|---|
| Piso de hall | Gris claro pulido (0.6, 0.6, 0.62) | Terrazo/porcelanato | Reutilizar `Terrazzo013` con tinte más claro (distinto del andén, que usa tono neutro) | 0.25 | 0.0 |
| Muros de hall | Blanco hueso (0.82, 0.8, 0.75) | Panel/pintura | Reutilizar `Tiles141` sin franja de color (a diferencia del andén, el hall es más "administrativo", menos identidad de línea) | 0.4 | 0.0 |
| Techo de hall | Gris panel (0.55, 0.55, 0.57) | Panel metálico | Nueva textura sugerida: ambientcg "MetalPlate" o reutilizar `Metal063` desaturado | 0.5 | 0.3 |
| Torniquetes | Metal plateado (0.7, 0.7, 0.72) | Acero inoxidable | Nueva textura sugerida: ambientcg "BrushedMetal" | 0.3 | 0.8 |
| Escaleras mecánicas | Metal oscuro (0.25, 0.25, 0.27) | Acero pintado | Reutilizar `Metal063` sin tinte óxido (aquí no debe verse oxidado, es zona "activa" aunque detenida) | 0.4 | 0.6 |
| Andén L5 — piso | Gris azulado (0.5, 0.52, 0.55) | Porcelanato moderno | Nueva textura o variante tintada de `Terrazzo013` | 0.3 | 0.0 |
| Andén L5 — muros/techo | Blanco frío panelado (0.75, 0.77, 0.8) | Panel compuesto | Nueva textura sugerida: ambientcg "CorrugatedSteel" o panel liso genérico | 0.35 | 0.2 |
| Mural "Ágora" | N/A (textura fotográfica) | Decal emissive bajo | Requiere imagen de referencia real (ver `referencias_fotograficas/11_Objetos`) — **no se puede generar sin la fuente real**, placeholder con textura de ruido en blanco/negro mientras tanto | N/A | N/A |
| Reja plataforma L7 | Metal oxidado oscuro (0.3, 0.28, 0.25) | Metal oxidado | Reutilizar `Metal063` con tinte oscuro — a diferencia de las rejas activas, esta debe verse **años sin mantenimiento** | 0.8 | 0.3 |

---

## 8. Iluminación

| Nombre | Tipo | Color | Intensidad | Función narrativa |
|---|---|---|---|---|
| Luz_Hall_Lineal (×6-8) | OmniLight3D o spot lineal | Blanco neutro (0.95, 0.95, 1.0) | Alta, uniforme | Iluminación "de oficina" pareja — sin la calidez del andén, más fría e institucional. Todas funcionando al inicio (esta zona nunca falla, a diferencia del andén) |
| Luz_Escalera (×2, una por tramo) | SpotLight3D | Blanco neutro | Media | Ilumina cada tramo de escalera |
| Luz_AndenL5 (×4-5) | OmniLight3D empotrada | Blanco frío (0.85, 0.9, 1.0) | Media-baja | Más tenue que el hall — transición gradual hacia la oscuridad del fondo (reja L7) |
| Luz_Emergencia_Hall (×2) | OmniLight3D roja | Rojo (mismo modelo que Andén L1) | Baja, permanente | Consistencia visual con el resto del juego |
| Ambient (WorldEnvironment) | Ambient light | Blanco-gris neutro (0.25, 0.25, 0.27) | Media | El hall es la zona MÁS iluminada del juego — refuerzo de que "todo parece normal" antes de que empiece a fallar en el andén |

**Regla de diseño:** a diferencia del Andén L1 (donde las luces fallan progresivamente), en el Hall **ninguna luz falla nunca**. Es la última zona de "seguridad total" antes de que el jugador cruce hacia el andén y el sistema de fallo de luces (`anden_baquedano.gd`) empiece a activarse.

---

## 9. Audio ambiental

| Categoría | Descripción | Comportamiento |
|---|---|---|
| Zumbido eléctrico de hall | Más grave y constante que el del andén (transformadores de mayor capacidad) | Loop continuo, reutilizar/adaptar `zumbido_electrico.wav` con pitch más bajo |
| Eco de pasos en hall abierto | Reverberación distinta (espacio más ancho y con techo bajo = eco más "plano" que el andén) | Bus de audio con reverb zone propia para el hall |
| Silencio de torniquetes | Ausencia deliberada de sonido de validación (deberían sonar "beep" al pasar, no suenan — nadie los ha usado en mucho tiempo) | Sin asset, es una ausencia de sonido, reforzada solo con texto/diseño |
| Goteo lejano hacia el andén L5 | Sonido de agua goteando, apenas audible, proveniente de la dirección de la reja L7 | Loop de baja prioridad, aumenta sutilmente cerca del elemento 16 |
| Transición de reverb L1→L5 | Cambio de firma acústica al cruzar el punto 13 (de reverb "hall abierto" a reverb "túnel cerrado") | Dos reverb zones con crossfade en el umbral |

---

## 10. Gameplay

| Elemento | Detalle |
|---|---|
| Spawn del jugador | En el acceso de mantenimiento (elemento 01), mirando hacia el sur (hacia el hall) |
| Eventos | Ninguno disparado por posición en esta zona (a diferencia del andén) — es zona de calma total, GDD exige curva ascendente, no se debe adelantar tensión aquí |
| Interacciones | Máquina Bip! (flavor text), mostrador de Bibliometro (nota opcional de lore — libro de préstamo con un nombre repetido varias veces), mapa de red (referencia visual, no crítico) |
| Objetos coleccionables | 1 nota opcional en Bibliometro (no obligatoria — GDD prioriza atmósfera sobre backtracking forzado) |
| Backtracking | El único backtracking real de todo el GDD ocurre aquí: el andén L5 es un callejón sin salida opcional, el jugador debe volver al hall para seguir hacia L1 |
| Punto de no retorno | Ninguno en esta zona — el punto de no retorno real sigue siendo el descenso a la vía en el Andén L1 (zona ya construida) |
| Conexión con zona existente | El elemento 11 (fin de escalera tramo 2) se conecta exactamente donde hoy está `Reja_Escalera_Norte` en `anden_baquedano.tscn` — en implementación, esa reja se retira o se abre |

---

## 11. Horror psicológico — cómo el escenario produce miedo

- **Contraste de escala:** el hall es el único espacio "grande y abierto" del juego — su vacío se siente más antinatural que el de espacios pequeños, porque un lugar diseñado para multitudes completamente solo rompe la expectativa de uso.
- **El mural "Ágora":** filas de rostros reales fotografiados observando pasillos vacíos — no se anima, no es sobrenatural, pero su sola presencia estática es perturbadora (el "uncanny" de rostros humanos inertes en un espacio sin gente).
- **Ausencia de sonido esperado:** los torniquetes no emiten el "beep" de validación — un silencio funcional roto es más inquietante que un silencio total.
- **La plataforma reservada de Línea 7 (elemento 16):** un espacio que **nunca ha operado**, sin luces, sin trenes, sin historia de uso — el liminal definitivo: ni siquiera pertenece al pasado de la estación, es un vacío que siempre estuvo vacío.
- **Contraste arquitectónico L1/L5:** el cambio de bóveda clásica a túnel panelado moderno, sin explicación textual, entrena al jugador a notar detalles arquitectónicos — preparación sutil para que perciba luego las anomalías del Andén L1.
- **Todo funciona "demasiado bien":** a diferencia del andén (donde las luces fallan), el hall está perfectamente iluminado y en silencio — la ausencia total de fallos aquí hace que el fallo posterior en el andén se sienta como una ruptura deliberada, no un accidente eléctrico genérico.

---

## 12. Optimización Godot 4

| Estrategia | Aplicación en este mapa |
|---|---|
| Sectores/Chunks | 2 sectores: `Hall` y `AndenL5` como nodos `Node3D` independientes, cargables/descargables por separado dado que L5 es opcional |
| Occlusion Culling | El pasillo de bifurcación (elemento 12) es un cuello de botella natural para `OccluderInstance3D` entre Hall y AndénL5 |
| LOD | Torniquetes y mobiliario de hall con LOD a 2 niveles (detalle completo <10m) |
| Static Bodies | Piso, muros, escaleras como `StaticBody3D` únicos por sector |
| Collision | Escaleras mecánicas con colisión de rampa simple (no geometría escalonada real, por rendimiento y porque el jugador las camina, no las usa activas) |
| NavigationRegion3D | Región separada para el hall (uso futuro si la entidad se expande a esta zona en versiones posteriores) |
| GridMap | Torniquetes (5 instancias idénticas) candidatos a `GridMap` |
| Instancing | Máquinas Bip!, basureros, extintores vía `PackedScene` reutilizada |

---

## 13. Organización del proyecto

```
linea_cero/
├── blender_pipeline/
│   └── hall_combinacion_l5/
│       └── generar_hall.py
├── assets/
│   ├── models/
│   │   └── hall_combinacion_l5/
│   │       └── hall_combinacion_l5.glb
│   ├── textures/
│   │   ├── mural_agora/          (requiere fuente real, ver sección 7)
│   │   ├── metal_moderno/        (nuevo, para L5 y torniquetes)
│   │   └── panel_techo/          (nuevo, para techos planos)
│   └── audio/
│       └── hall_combinacion_l5/
│           ├── zumbido_hall.wav
│           ├── goteo_lejano.wav
│           └── reverb_transicion.wav
├── scenes/
│   └── hall_combinacion_l5.tscn
├── scripts/
│   └── hall_combinacion_l5.gd    (mínimo — sin eventos de tensión)
└── design_docs/
    └── MAPA_HallCombinacionL5.md (este documento)
```

---

## 14. Checklist de producción (mínimo 100 puntos)

### Investigación y fuentes (8)
- [ ] 1. Confirmar dimensiones reales de hall si aparece plano oficial (actualmente estimado)
- [ ] 2. Conseguir imagen real del mural "Ágora" para textura (actualmente sin fuente, ver sección 7)
- [ ] 3. Fotografiar o conseguir referencia de escaleras mecánicas reales de Baquedano
- [ ] 4. Confirmar perfil arquitectónico real de andén L5 (actualmente estimado por inferencia constructiva)
- [ ] 5. Verificar color/diseño actual de franja identificadora con foto reciente (post-2024)
- [ ] 6. Confirmar diferencia de profundidad real entre L1 y L5 si aparece dato público
- [ ] 7. Revisar las 5 versiones históricas de "Cenefa Metro Baquedano" en Wikimedia Commons para elegir la más representativa
- [ ] 8. Descargar los ~35-40 archivos ya identificados en `referencias_fotograficas/README.md`

### Blockout (12)
- [ ] 9. Piso y techo de hall a escala 20×25×4.5m
- [ ] 10. 4 muros perimetrales con huecos correctos (accesos, escaleras, bifurcación L5)
- [ ] 11. Volúmenes de torniquetes (5), boletería, Bibliometro, local comercial
- [ ] 12. Dos tramos de escalera + descanso intermedio con diferencia de altura de 10m total
- [ ] 13. Pasillo de bifurcación hacia L5
- [ ] 14. Piso y techo de andén L5 a -10m relativo al hall
- [ ] 15. Reja de plataforma reservada L7 al fondo del andén L5
- [ ] 16. Verificación de escala caminando con el player controller
- [ ] 17. Punto de conexión sur alineado exactamente con `Reja_Escalera_Norte` del Andén L1 existente
- [ ] 18. Sin overlaps de colisión entre zonas (lección de la sección 16/18 del documento del Andén aplicada aquí)
- [ ] 19. Colisión de escaleras probada (rampa simple, sin escalones reales)
- [ ] 20. Transición de nivel (nueva escena vs. misma escena que Andén L1) decidida y documentada

### Materiales (10)
- [ ] 21. Piso de hall con material distinto (más claro) al del andén
- [ ] 22. Muros de hall sin franja de color (distinción deliberada del andén)
- [ ] 23. Techo panelado (no bóveda) correctamente materializado
- [ ] 24. Material de torniquetes (acero inoxidable, sin óxido)
- [ ] 25. Material de escaleras mecánicas (acero pintado, sin óxido — a diferencia de rejas del andén)
- [ ] 26. Piso y muros de andén L5 con material distinto al de L1 (contraste arquitectónico)
- [ ] 27. Textura de mural "Ágora" aplicada (real o placeholder documentado)
- [ ] 28. Reja de plataforma L7 con óxido pronunciado (años sin mantenimiento)
- [ ] 29. Verificación de que ningún material usa parallax/heightmap (lección de Sala Técnica)
- [ ] 30. Coherencia de paleta entre las 3 zonas (Sala Técnica, Hall, Andén) revisada en conjunto

### Iluminación (10)
- [ ] 31. 6-8 luces lineales de hall, blancas, uniformes, todas encendidas
- [ ] 32. Ninguna luz del hall falla nunca (regla de diseño de la sección 8)
- [ ] 33. Luces de escalera en ambos tramos
- [ ] 34. Luces de andén L5 más tenues que el hall, gradiente hacia oscuridad en el fondo
- [ ] 35. 2 luces de emergencia rojas reutilizando el modelo del Andén L1
- [ ] 36. Ambient light configurado (más brillante que el andén, refuerza "todo normal aquí")
- [ ] 37. Verificación de que `light_energy` (no `light_energy_multiplier`) se usa en todas las luces nuevas — bug ya documentado en Andén Baquedano sección 17
- [ ] 38. Transición de iluminación gradual entre hall y andén L5 (sin corte abrupto)
- [ ] 39. Reja de plataforma L7 sin ninguna luz (oscuridad total deliberada)
- [ ] 40. Prueba de legibilidad general caminando la zona completa

### Audio (8)
- [ ] 41. Zumbido de hall (grave, distinto al del andén) en loop
- [ ] 42. Reverb zone propia del hall (eco "plano" de espacio ancho y techo bajo)
- [ ] 43. Ausencia deliberada de sonido de validación en torniquetes verificada
- [ ] 44. Goteo lejano cerca de la reja de plataforma L7
- [ ] 45. Reverb zone de andén L5 distinta a la del hall
- [ ] 46. Crossfade de reverb en el umbral hall→L5 (elemento 13) sin corte brusco
- [ ] 47. Mezcla general probada con auriculares y parlantes
- [ ] 48. Ningún audio de esta zona dispara eventos de tensión prematuros (regla GDD: curva ascendente)

### Props y set dressing (10)
- [ ] 49. 5 torniquetes colocados en fila
- [ ] 50. Mostrador de boletería
- [ ] 51. Mostrador y estantería de Bibliometro
- [ ] 52. Cajero automático
- [ ] 53. Vitrina de local comercial vacío
- [ ] 54. 2-3 máquinas de carga Bip!
- [ ] 55. Basureros y extintor de estilo hall (distinto al del andén)
- [ ] 56. Mapa de red genérico en pared
- [ ] 57. Señalética de accesos A-D
- [ ] 58. Letrero "PLATAFORMA RESERVADA — LÍNEA 7"

### Gameplay y narrativa (12)
- [ ] 59. Spawn del jugador en acceso de mantenimiento, orientación correcta
- [ ] 60. Interacción con máquina Bip! (flavor text)
- [ ] 61. Interacción con Bibliometro (nota opcional de lore)
- [ ] 62. Recorrido completo probado sin softlocks
- [ ] 63. Backtracking del andén L5 confirmado como no obligatorio pero accesible
- [ ] 64. Conexión con Andén L1 probada sin cortes visuales
- [ ] 65. Ningún evento de tensión disparado en el hall (verificado con playtesting)
- [ ] 66. Tiempo de recorrido real medido, dentro de 3-6 min
- [ ] 67. Punto de conexión con `Reja_Escalera_Norte` actualizado en `anden_baquedano.tscn` (retirar o abrir la reja)
- [ ] 68. Coherencia narrativa: el jugador entiende que llegó de Sala Técnica sin necesidad de exposición forzada
- [ ] 69. La plataforma L7 se percibe como misteriosa sin necesidad de texto explicativo
- [ ] 70. Ningún jump scare presente en ninguna iteración de prueba

### Optimización (10)
- [ ] 71. Sectores Hall y AndénL5 como nodos independientes
- [ ] 72. Occlusion culling en el pasillo de bifurcación
- [ ] 73. LOD en torniquetes y mobiliario
- [ ] 74. Static bodies consolidados por sector
- [ ] 75. Colisión de escaleras simplificada (rampa, no escalones)
- [ ] 76. NavigationRegion3D del hall generado (para uso futuro)
- [ ] 77. Torniquetes evaluados para GridMap
- [ ] 78. Props repetidos usando instancias de escena
- [ ] 79. Draw calls verificados con profiler antes de aprobar
- [ ] 80. Memoria de texturas verificada (sin duplicar Terrazzo013/Metal063 innecesariamente)

### QA general (5)
- [ ] 81. Probado con godot-ai (ejecución real + captura + logs), no solo revisión de código
- [ ] 82. Sin errores en logs tras ejecución continua de al menos 30s
- [ ] 83. Playtesting con al menos 2 personas ajenas al desarrollo
- [ ] 84. Verificación de que el hall no rompe el ritmo total del GDD (25-40 min)
- [ ] 85. Documento actualizado con cualquier desviación encontrada durante implementación (siguiendo el precedente de la sección 16/18 del Andén Baquedano)

---

## 15. Adaptaciones de gameplay (justificación de desvíos respecto a la realidad)

| Desvío de la realidad | Justificación |
|---|---|
| Andén L5 modelado a 60m en vez de escala completa (~95-110m como L1) | Esta zona es de atmósfera y contraste arquitectónico, no de gameplay central — el GDD no requiere que el jugador recorra la totalidad del andén L5, solo que lo perciba y decida volver |
| Pasillo de mantenimiento entre Sala Técnica y este Hall no detallado en este documento | Requiere su propio documento de diseño si se decide detallarlo; por ahora se asume una transición de escena directa, consistente con el patrón ya usado entre Sala Técnica y Andén L1 |
| Mural "Ágora" sin fuente fotográfica real disponible | Documentado explícitamente como pendiente (checklist ítem 2) — se usa placeholder hasta conseguir la imagen real, no se inventa el contenido del mural |
| Diferencia de profundidad L1↔L5 estimada en 10m sin fuente exacta | Ninguna fuente pública consultada especifica la cota exacta; 10m es un valor plausible para 2 tramos de escalera mecánica estándar, consistente con "numerosas escaleras" confirmado en las fuentes |
| Esta zona no reconstruye el Hall real al 100% (omite detalles como iluminación exacta, mobiliario específico, cantidad exacta de torniquetes) | Igual que el Andén Baquedano (sección 18.3 de ese documento), se prioriza la función narrativa del GDD sobre la reconstrucción arquitectónica exhaustiva — esta es una decisión consciente, no una limitación oculta |

---

**FIN DEL DOCUMENTO — Fase 2 completa.**

Según el proceso establecido, corresponde ahora **esperar aprobación** antes de iniciar la Fase 3 (Implementación: blockout → iluminación → materiales → props → audio → navegación → gameplay en Blender/Godot, en ese orden, sin mezclar fases).
