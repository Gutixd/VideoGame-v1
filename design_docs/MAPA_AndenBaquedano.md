# MAPA_AndenBaquedano.md

**Proyecto:** LÍNEA CERO
**Zona:** 02 — Andén Baquedano
**Autor:** Senior Level Designer / Environment Artist (documento de diseño)
**Estado:** 🟡 Pendiente de aprobación — NO IMPLEMENTAR hasta visto bueno
**Versión:** 1.0

---

## 0. Fuente de investigación (Fase 1)

Basado en el estilo arquitectónico documentado de las estaciones originales de Metro de Santiago Línea 1 (1975): Los Héroes, Universidad de Chile, Salvador — comparables directas a Baquedano por pertenecer al mismo tramo y década constructiva. Ver tabla de hallazgos en el research previo a este documento. Toda medida sin fuente pública exacta está marcada **[ESTIMADO]**.

---

## 1. Información general

| Campo | Valor |
|---|---|
| Nombre | Andén Baquedano |
| Zona (GDD) | 02 — Andén Baquedano |
| Objetivo narrativo | Establecer que la estación está completamente vacía y que algo no está bien. Primer contacto auditivo (no visual) con la entidad. Transición de "normalidad" a "amenaza latente" |
| Objetivo del jugador | Cruzar el andén de extremo a extremo, investigar el panel de llegadas y la caseta de control, encontrar el punto de descenso a las vías que conduce al Túnel km 1.4 |
| Duración estimada | 5–15 min (según GDD) |
| Nivel de tensión | Bajo → Medio (curva ascendente). Empieza en calma aparente, termina con el jugador dudando de su percepción |
| Inspiración | P.T. (repetición/quiebre de expectativa), Chilla's Art (estación vacía), Backrooms (iluminación fluorescente uniforme y silencio opresivo) |

---

## 2. Medidas

| Elemento | Medida real estimada | Medida usada en el nivel | Justificación |
|---|---|---|---|
| Largo total del andén | ~95–110 m [ESTIMADO] | **55 m** | Ver "Adaptaciones de Gameplay" — comprimido para ritmo de horror, resto implícito con oscuridad/niebla en extremos bloqueados |
| Ancho útil de andén (isla) | ~6–8 m [ESTIMADO] | 7 m | Dentro de rango real, permite recorrido cómodo en primera persona sin sentirse angosto |
| Ancho de cada vía (foso) | ~3.5 m [ESTIMADO] | 3.5 m | Sin cambios, es dimensión funcional de riel estándar |
| Ancho total estación (vía+andén+vía) | ~12–14 m [ESTIMADO] | 14 m | Ancho total = 3.5 + 7 + 3.5 |
| Alto libre en muros laterales | ~4.2–4.5 m [ESTIMADO] | 4.3 m | — |
| Alto en clave de bóveda (centro) | ~5.5 m [ESTIMADO] | 5.5 m | Curvatura de bóveda de cañón |
| Separación entre columnas | ~6 m [ESTIMADO, basado en proporción foto] | 6 m | 9 columnas a lo largo de 55 m |
| Altura de borde de andén sobre riel | ~1.1 m | 1.1 m | Estándar de seguridad ferroviaria |
| Escala real | 1 unidad Godot = 1 metro | — | Estándar del proyecto |

---

## 3. Plano superior (planta técnica)

Vista en planta, jugador entra por el Norte (desde Sala Técnica) y sale por el Sur (hacia Túnel km 1.4).

```
NORTE (entrada desde Sala Técnica)
│
│   ┌─────────────────────────────────────────────────────────────────┐
│   │ 01                                                          02  │  ← Muro Norte (cierre de nivel, escaleras clausuradas)
│   ├─────────────────────────────────────────────────────────────────┤
│ 03│░░░░░░░░░░░░░░░░░░░░░░░░ VÍA 1 (foso, no transitable) ░░░░░░░░░░░│03
│   ├──┬────────┬────────┬────────┬────────┬────────┬────────┬──┬────┤
│   │  │  05    │        │  06    │        │  07    │        │  │    │
│   │04│ (col)  │        │ (col)  │  08    │ (col)  │        │04│ 09 │  ← ANDÉN (zona jugable)
│   │  │        │        │        │        │        │        │  │    │
│   ├──┴────────┴────────┴────────┴────────┴────────┴────────┴──┴────┤
│10 │░░░░░░░░░░░░░░░░░░░░░░░░ VÍA 2 (foso, no transitable) ░░░░░░░░░░░│10
│   ├─────────────────────────────────────────────────────────────────┤
│   │ 11                                                          12  │  ← Muro Sur / boca de túnel (punto de no retorno)
│   └─────────────────────────────────────────────────────────────────┘
│
SUR (hacia Túnel km 1.4)
```

### Leyenda numerada

| # | Elemento | Descripción funcional |
|---|---|---|
| 01 | Escalera mecánica Norte (clausurada) | Bloqueada con reja + letrero "FUERA DE SERVICIO". Cierra el nivel por el norte sin necesidad de modelar la mezzanine completa |
| 02 | Escalera fija de emergencia Norte | Misma función que 01, variante visual, refuerza sensación de instalación real con dos accesos |
| 03 | Vía 1 (foso norte→sur, lado oeste) | No transitable en esta zona. Visualmente debe verse el riel, durmientes, balasto y cable de tercer riel |
| 04 | Extremo del andén (barrera de seguridad) | Reja baja + señalética de "no pasar". Marca el límite físico jugable en ambos extremos laterales |
| 05, 06, 07 | Columnas estructurales (3 de 9 visibles en el corte) | Soportan la bóveda, dividen visualmente el recorrido en tramos, usadas para line-of-sight y ocultamiento de sustos no-jumpscare (siluetas, sombras) |
| 08 | Caseta de control / kiosco de andén | Punto de interacción: aquí está el panel de llegadas y la radio secundaria. Estructura pequeña 2×2 m adosada a la columna 06 |
| 09 | Banca de espera + basurero | Prop de ambientación, reutilizable en todo el tramo |
| 10 | Vía 2 (foso norte→sur, lado este) | Simétrica a 03 |
| 11 | Muro Sur — Boca de túnel Oeste | Uno de los dos túneles reales de la vía. Aquí el jugador **desciende al riel** para iniciar la zona 03 (Túnel km 1.4) |
| 12 | Muro Sur — Boca de túnel Este | Boca del túnel opuesto, sellada con reja "SIN SALIDA" — refuerza que solo hay un camino posible (diseño lineal encubierto) |

**Elementos adicionales no marcados en el plano (por claridad), pero presentes:**
- Panel de llegadas LED, suspendido del techo sobre el centro del andén (entre columnas 06 y 07)
- 3 carteles colgantes con el nombre "BAQUEDANO" repetidos cada ~15 m
- Franja táctil amarilla continua en ambos bordes del andén (03/10)
- Luminarias lineales en cornisa de bóveda, 1 cada 6 m (alineadas a columnas)

---

## 4. Vista isométrica (descripción)

El jugador entra por el extremo norte a través de una abertura enrejada (antigua escalera de acceso, ahora clausurada — refuerzo narrativo de que la única salida "normal" ya no existe). Desde ahí, la vista isométrica muestra:

- **Volumen dominante:** la bóveda de cañón continua, que unifica visualmente todo el tramo — no hay quiebres de techo, lo que genera un pasillo de fuga visual muy largo (comprimido a 55 m pero siempre percibido como "más largo" gracias a niebla volumétrica en ambos extremos).
- **Simetría opresiva:** las columnas (05-07 y sus pares no numerados) crean un ritmo repetitivo idéntico a ambos lados, lo cual es intencional: la simetría perfecta en espacios liminales genera desorientación subconsciente (referencia directa a Backrooms).
- **Líneas de visión:** desde el punto de entrada norte, el jugador tiene visión directa de ~40 m del andén (hasta que la niebla/oscuridad corta la visibilidad cerca del extremo sur), pero **no** puede ver la boca del túnel (11) hasta recorrer aproximadamente 2/3 del andén — esto es deliberado: la "meta" del nivel se revela tarde para sostener el dread acumulativo del GDD.
- **Contraste de alturas:** el foso de vías (03/10) está 1.1 m bajo el nivel del andén, lo que en primera persona genera una sensación de "borde/precipicio" sutil cada vez que el jugador se acerca al límite — usado para tensión ambiental sin necesidad de peligro real de caída (no hay gameplay de combate/caída según GDD).
- **Recorrido:** estrictamente lineal norte→sur sobre el andén; el único momento de decisión real es al final, cuando el jugador debe bajar al riel por la boca oeste (11) — la boca este (12) está bloqueada, eliminando ambigüedad de navegación pero manteniéndola visualmente presente (refuerza el "no hay otra salida").

---

## 5. Blockout (solo cajas — sin detalle)

Todas las posiciones son relativas al origen del nivel (0,0,0 = centro del andén a nivel del piso, eje +Z hacia el Sur/túnel, eje +X hacia el Este).

| Nombre | Tipo de caja | Posición (X,Y,Z) | Escala (L×A×Alto) | Rotación | Función |
|---|---|---|---|---|---|
| BLOCK_Piso_Anden | Box | (0, 0, 0) | 7 × 55 × 0.2 | 0° | Piso caminable del andén |
| BLOCK_Muro_Norte | Box | (0, 2.15, -27.5) | 14 × 0.5 × 4.3 | 0° | Cierre norte del nivel |
| BLOCK_Muro_Sur_Oeste | Box | (-3.5, 2.15, 27.5) | 3.5 × 0.5 × 4.3 | 0° | Mitad oeste del muro sur (deja hueco = boca de túnel 11) |
| BLOCK_Muro_Sur_Este | Box | (3.5, 2.15, 27.5) | 3.5 × 0.5 × 4.3 | 0° | Mitad este del muro sur (deja hueco = boca de túnel 12, bloqueada con reja) |
| BLOCK_Boveda | Cylinder (mitad, orientado) | (0, 4.3, 0) | radio 7, largo 55 | eje X | Techo abovedado, un solo volumen continuo |
| BLOCK_Foso_Via1 | Box (vacío/hundido) | (-5.25, -0.55, 0) | 3.5 × 55 × 1.1 | 0° | Volumen de la vía oeste, 1.1 m bajo andén |
| BLOCK_Foso_Via2 | Box (vacío/hundido) | (5.25, -0.55, 0) | 3.5 × 55 × 1.1 | 0° | Volumen de la vía este |
| BLOCK_Columna_01..09 | Box (×9) | X=0 (centro andén), Z = -24, -18, -12, -6, 0, 6, 12, 18, 24 | 0.6 × 0.6 × 4.3 c/u | 0° | Columnas estructurales, separación real 6 m |
| BLOCK_Caseta_Control | Box | (1.5, 1.1, 0) | 2 × 2 × 2.2 | 0° | Volumen del kiosco/caseta (adosado a columna 05) |
| BLOCK_Barrera_Oeste | Box (×2, extremos) | (-3.4, 0.5, ±26) | 0.3 × 0.6 × 1.0 | 0° | Barrera de seguridad borde andén, extremo norte y sur |
| BLOCK_Barrera_Este | Box (×2, extremos) | (3.4, 0.5, ±26) | 0.3 × 0.6 × 1.0 | 0° | Idem lado este |
| BLOCK_Reja_Escalera_Norte | Box | (0, 1.5, -27.3) | 3 × 0.1 × 3 | 0° | Bloqueo visual de escalera clausurada (elemento 01) |
| BLOCK_Reja_TunelEste | Box | (3.5, 2.15, 27.3) | 3.5 × 0.1 × 4 | 0° | Bloqueo de boca de túnel este (elemento 12) |
| BLOCK_Panel_Llegadas | Box (suspendida) | (0, 3.6, -3) | 2.5 × 0.2 × 0.8 | 0° | Volumen del panel LED, colgado del techo |
| BLOCK_Descenso_Via | Box (rampa/escalón) | (-2, -0.3, 26) | 2 × 1.5 × 1.1 | 0° | Marca el punto exacto donde el jugador puede descender al riel hacia el Túnel km 1.4 |

**Nota de blockout:** en esta fase NO se incluyen tuberías, cableado, bancas, basureros, carteles ni luminarias de detalle — solo se listan en la sección de Assets para fase posterior.

---

## 6. Lista completa de Assets

### Arquitectura
- Losa de piso de andén (con junta de dilatación cada ~10 m)
- Muro curvo de bóveda (segmento repetible, modular cada 6 m para instancing)
- Muro bajo (zócalo) de andén, altura 1.2 m, remate superior distinto material
- Columna estructural rectangular (modular, 9 instancias)
- Borde de andén con canto de terrazo/granito oscuro
- Foso de vía: durmientes de hormigón, riel metálico, balasto (grava), cable de tercer riel
- Boca de túnel (arco de entrada, oeste transitable / este sellado)
- Reja metálica de bloqueo (2 variantes: escalera clausurada, túnel sellado)
- Caseta de control (kiosco), incluye puerta, ventanilla, mostrador interior

### Props
- Banca de espera (modular, 4 instancias a lo largo del andén)
- Basurero metálico (3 instancias)
- Extintor de incendios en muro (2 instancias, junto a columnas)
- Caja de herramientas abandonada de Rodrigo (prop narrativo, cerca del punto de descenso — plantar pista de lore)
- Nota de otro técnico (prop interactivo, sobre la banca cerca de la caseta — lore del GDD)
- Radio secundaria (prop interactivo dentro de la caseta)
- Reloj de andén analógico (detenido en una hora específica — detalle de horror sutil)

### Iluminación (objetos físicos, no las luces en sí — ver sección 8)
- Luminaria lineal de cornisa (modular, 1 cada 6 m, alineada a columnas) — 9 instancias
- Luminaria de emergencia roja (modular, 4 instancias repartidas, funciona incluso si el resto falla — ver iluminación narrativa)

### Señalética
- Cartel colgante "BAQUEDANO" (3 instancias)
- Placa de nombre en columna (9 instancias, una por columna)
- Señal "NO PASAR" en barreras de extremo (4 instancias)
- Señal "FUERA DE SERVICIO" en escalera norte
- Señal "SIN SALIDA" en boca de túnel este
- Panel de llegadas LED (1 instancia, prop interactivo clave del GDD — "muestra trenes que no existen en el horario")
- Franja táctil amarilla (mesh de piso, textura decal, corre todo el borde de andén)

### Cableado
- Bandeja de cables en cornisa superior (corre paralela a las luminarias)
- Conducto eléctrico expuesto bajando por columnas cada 3 columnas

### Tuberías
- Tubería de ventilación/drenaje, diámetro mayor, corre por el cielo de la bóveda en el eje longitudinal
- Válvula de purga (detalle, cerca de la caseta de control)

### Equipos eléctricos
- Tablero eléctrico (adosado a muro, cerca de columna 07)
- Caja de breakers (dentro de la caseta de control)

### Basura / Detalle sucio
- Papeles y desechos dispersos (decals + mesh simple, 6-8 instancias dispersas)
- Manchas de humedad en muro y techo (decals)
- Óxido en rejas y estructuras metálicas (parte del material, no mesh aparte)

### Mobiliario
- Mostrador interior de caseta de control
- Silla de vigilante (caída/volcada — detalle narrativo de abandono repentino)

### Puertas
- Puerta de caseta de control (simple, batiente)

### Ventilación
- Rejilla de ventilación en muro bajo (3 instancias, puramente decorativas)

### Techo
- Bóveda de hormigón visto (ver Blockout, elemento BLOCK_Boveda)
- Cornisa perimetral (alberga cableado + luminarias)

### Piso
- Losa de andén (terrazo pulido gris)
- Franja táctil amarilla (borde)
- Balasto de vía (grava suelta, mesh + textura tileable)

### Paredes
- Zócalo cerámico crema (parte baja de muro)
- Franja de color identificador ocre/mostaza (parte alta de muro) **[color estimado, ver sección Materiales]**

---

## 7. Materiales

| Objeto | Color | Material | Textura (fuente sugerida) | Roughness | Metallic | Normal Map |
|---|---|---|---|---|---|---|
| Piso andén (terrazo) | Gris medio (0.55, 0.55, 0.57) | Terrazo pulido | ambientcg "Marble" o "Terrazo" tileado | 0.35 (pulido, algo de brillo) | 0.0 | Sí, sutil |
| Franja táctil (borde andén) | Amarillo tráfico (0.85, 0.7, 0.05) | Caucho/pintura antideslizante | Textura procedural o ambientcg "RubberFloor" | 0.6 | 0.0 | Sí, relieve de puntos |
| Zócalo cerámico (muro bajo) | Crema/hueso (0.85, 0.8, 0.7) | Cerámica esmaltada | ambientcg "Tiles" variante clara, tinte albedo | 0.3 | 0.0 | Sí (líneas de junta) |
| Franja de color identificador (muro alto) | Ocre/mostaza **[estimado]** (0.75, 0.55, 0.15) | Cerámica esmaltada mate | Igual base que zócalo, tinte distinto | 0.35 | 0.0 | Sí |
| Bóveda de hormigón | Gris cálido (0.5, 0.48, 0.45) | Hormigón visto | ambientcg "Concrete034" (ya usado en Sala Técnica, mantiene coherencia) | 0.85 | 0.0 | Sí |
| Columnas estructurales | Gris oscuro pintado (0.35, 0.35, 0.37) | Hormigón pintado | Variante tinte de Concrete034 | 0.6 | 0.0 | Sí |
| Riel metálico | Metal grafito con brillo de uso (0.3, 0.3, 0.32) | Acero pulido por fricción | ambientcg "Metal" variante pulida | 0.3 | 0.85 | Sí |
| Durmientes de vía | Hormigón oscuro envejecido (0.25, 0.24, 0.22) | Hormigón/madera tratada | ambientcg "Concrete" variante sucia | 0.9 | 0.0 | Sí |
| Balasto (grava) | Gris-marrón variado (0.4, 0.37, 0.33) | Piedra suelta | ambientcg "Gravel" | 0.95 | 0.0 | Sí (relieve fuerte, sin parallax — lección aprendida en Sala Técnica) |
| Rejas metálicas de bloqueo | Metal oxidado marrón-óxido (0.55, 0.35, 0.2) | Metal oxidado | Reutilizar `Metal063` ya en proyecto (assets/textures/metal_oxidado) | 0.7 | 0.4 | Sí |
| Caseta de control | Crema con base metálica (0.8, 0.75, 0.65) / metal gris | Panel prefabricado + metal | Mixto zócalo + Metal063 | 0.5 | 0.2 (partes metálicas) | Sí |
| Panel de llegadas (carcasa) | Negro mate (0.05, 0.05, 0.06) | Plástico/metal mate | StandardMaterial3D plano + emisión en pantalla | 0.4 | 0.3 | No necesario |
| Panel de llegadas (pantalla) | Emisivo ámbar (1.0, 0.6, 0.1) | Emissive | Textura de texto LED simple | N/A | N/A | No |
| Bancas | Madera envejecida + metal (0.45, 0.3, 0.2) | Madera tratada + acero | ambientcg "Wood" + Metal063 | 0.6 | 0.1 | Sí |
| Cartel colgante / placas | Azul marino (0.05, 0.08, 0.2) fondo, texto blanco | Metal pintado + Label3D o textura de texto | Plano simple, texto via Label3D (igual método que Sala Técnica) | 0.4 | 0.1 | No |

**Nota de coherencia:** Se reutilizan deliberadamente `Concrete034` y `Metal063` ya descargados para Sala Técnica (misma carpeta `assets/textures/`), evitando duplicar descargas y manteniendo consistencia visual entre zonas del mismo edificio/estación.

---

## 8. Iluminación

| Nombre | Tipo | Color | Temperatura aprox. | Intensidad | Radio/Alcance | Sombras | Función narrativa |
|---|---|---|---|---|---|---|---|
| Luz_Cornisa_01..09 | OmniLight3D (o spot lineal) | Blanco cálido (1.0, 0.95, 0.85) | ~3800K | 0.9 (normalizada) | 6 m | Activadas | Iluminación "normal" funcionando al inicio — parte de la ilusión de que todo está bien |
| Luz_Cornisa_Fallando (subset de las anteriores, ~40%) | OmniLight3D con script de parpadeo | Blanco cálido → parpadeo a frío | ~3800K variable | 0.9 → 0.0 intermitente | 6 m | Activadas | "Luces que fallan en secuencia" — GDD explícito. Se activa progresivamente mientras el jugador avanza, nunca todas a la vez |
| Luz_Emergencia_01..04 | OmniLight3D | Rojo (1.0, 0.15, 0.1) | N/A (coloreada) | 0.5 | 4 m | Desactivadas (luz de ambiente, no debe generar sombras duras) | Permanece encendida SIEMPRE, incluso cuando fallan las cornisas — ancla visual de "esto es una emergencia constante" |
| Luz_Panel_Llegadas | Emissive (material, no luz real) | Ámbar (1.0, 0.6, 0.1) | N/A | Emission energy 2.5 | Local | N/A | Punto focal de interacción — atrae la mirada del jugador hacia el prop clave |
| Luz_Boca_Tunel_Oeste | SpotLight3D, apuntando hacia adentro del túnel | Blanco frío tenue (0.7, 0.75, 0.8) | ~5500K | 0.3 | 8 m (cono largo, angosto) | Activadas | Sugiere profundidad sin revelar el túnel — genera curiosidad/temor anticipado antes de la zona 03 |
| Ambient (WorldEnvironment) | Ambient light | Gris-azulado frío (0.15, 0.16, 0.18) | N/A | 0.25 | Global | N/A | Evita negros absolutos fuera del alcance de luces puntuales, manteniendo legibilidad sin romper el horror (no queremos oscuridad total en esta zona, esa es la función del Túnel) |

**Diseño de secuencia de fallo (crítico para el GDD):** las luces de cornisa deben fallar en un patrón que el jugador pueda percibir como "casi aleatorio pero no del todo" — recomendación de implementación futura (NO código ahora): activar el fallo de una luz cada vez que el jugador cruza cierto umbral de Z, siempre en la luz más cercana a su posición actual, nunca por delante de él. Esto crea la sensación de que "algo apaga las luces detrás de mí".

---

## 9. Audio ambiental

| Categoría | Descripción | Comportamiento |
|---|---|---|
| Ruido ambiente base | Zumbido eléctrico bajo constante (transformadores/luminarias), muy sutil, casi subliminal | Loop continuo, volumen bajo (-30dB aprox.) |
| Electricidad | Chisporroteo breve sincronizado con cada luz de cornisa que falla | Disparado por evento, no loop |
| Viento/corriente de aire de túnel | Soplo grave y prolongado, proveniente específicamente de la boca oeste (11) | Aumenta en volumen a medida que el jugador se acerca al extremo sur |
| Túneles (reverberación de fondo) | Eco lejano indefinido, imposible de identificar como paso o goteo | Loop de baja prioridad, aumenta sutilmente con la proximidad a las bocas de túnel |
| Trenes | **"El tren que nunca llega pero siempre se escucha venir"** (cita directa del GDD) — sonido de tren acercándose que se desvanece antes de llegar, 1-2 veces durante el recorrido | Disparado por trigger de posición, no debe repetirse en el mismo punto exacto dos veces en una partida |
| Radio | Estática que sube al acercarse a la caseta de control (elemento 08); voz del operador con frases cada vez más cortadas | Vinculado a la mecánica de Radio de mano del GDD, aquí tiene su primer punto de interacción física (la radio secundaria en la caseta) |
| Pasos (del jugador) | Pisada sobre terrazo — sonido "limpio" y nítido, contraste total con lo que vendrá en el Túnel | Estándar, sin delay ni eco excesivo — la ausencia de anomalía sonora aquí es intencional, contraste con zona 03 |
| Reverberación general | Reverb de espacio grande/duro (hormigón), tiempo de decaimiento medio-largo (~1.8s) | Bus de audio con reverb zone abarcando todo el andén |
| Primer contacto auditivo con la entidad (GDD) | Sonido no identificable, muy breve (<1s), ocurre una sola vez, en un punto fijo cercano al final del andén (cerca de columna 08-09), nunca visible | Trigger único por partida, no debe repetirse ni tener contraparte visual |

---

## 10. Gameplay

| Elemento | Detalle |
|---|---|
| Spawn del jugador | Justo pasando la reja de la escalera norte (elemento 01), mirando hacia el sur (hacia el andén) |
| Eventos | (1) Secuencia de fallo de luces progresivo; (2) Sonido de tren fantasma 1-2 veces; (3) Primer contacto auditivo con la entidad cerca del extremo sur |
| Puzzles | Ninguno explícito — el GDD no contempla puzzles duros en V1, esta zona es de exploración/tensión, no de resolución de acertijos |
| Llaves | No aplica en esta zona |
| Interacciones | Panel de llegadas (elemento del kiosko 08) — mostrar horario con trenes inexistentes; Radio secundaria (dentro de 08); Nota de técnico (prop sobre banca 09) |
| Objetos coleccionables | 1 nota de lore (obligatoria de encontrar o al menos visible en el camino, no oculta en exceso — GDD prioriza atmósfera sobre backtracking forzado) |
| Backtracking | Ninguno — diseño estrictamente lineal norte→sur, consistente con "Cuatro zonas lineales con algo de backtracking" del GDD (el backtracking ocurre en otras zonas, no aquí) |
| Puntos de tensión | (a) Cruce del primer tercio a oscuras si la luz de cornisa más cercana ya falló; (b) Acercamiento a la boca de túnel este bloqueada (12) — falso indicio de alternativa; (c) Momento exacto del contacto auditivo con la entidad |
| Zonas seguras | El tramo inicial (primeros ~15 m desde el spawn) debe mantenerse siempre iluminado — zona de "respiro" antes de que empiece el fallo de luces |
| Punto de no retorno | Descenso a la vía por la boca oeste (elemento 11 / BLOCK_Descenso_Via) — una vez el jugador baja, no puede volver a subir al andén (consistente con "Punto de no retorno" de la zona 03 del GDD) |

---

## 11. Horror psicológico — cómo el escenario produce miedo

Sin jumpscares, sin entidad visible, siguiendo estrictamente el GDD:

- **Arquitectura:** la simetría perfecta y repetitiva de columnas/bóveda genera desorientación sutil — el cerebro espera variación y no la encuentra, lo que produce incomodidad de bajo nivel constante (efecto "uncanny" de espacio liminal).
- **Silencio:** el contraste entre el "ruido normal" (zumbido eléctrico, pasos limpios) y los micro-silencios que preceden a cada evento (fallo de luz, tren fantasma) entrena al jugador a temer el silencio mismo.
- **Iluminación:** el fallo progresivo de luces —siempre detrás del jugador, nunca delante— crea la sensación de estar siendo "cerrado" o "seguido" sin mostrar nada. Las luces rojas de emergencia que nunca se apagan generan un ancla visual perturbadora (siempre hay una fuente de luz, pero es la señal de que algo va mal, no de seguridad).
- **Distancias:** el largo comprimido de 55 m sigue siendo lo bastante extenso para que el jugador nunca vea ambos extremos del andén simultáneamente con claridad — la niebla en los extremos hace que la distancia percibida sea mayor a la real, jugando con la escala.
- **Perspectiva:** la altura de la bóveda (5.5 m en el centro vs 4.3 m en muros) hace que el techo "se sienta" opresivamente bajo pese a ser generoso en metros — un truco de proporción, no de tamaño absoluto.
- **Audio:** el "tren que nunca llega" es el ejemplo más directo de expectativa rota — el jugador anticipa un evento (tren llegando) basado en lógica real (esto es una estación de metro) y esa expectativa nunca se cumple, lo cual es más inquietante que si nunca hubiera sonido de tren en absoluto.
- **Espacios liminales:** el andén es, por definición, un espacio de tránsito, no de permanencia — un lugar diseñado para estar vacío de gente en su uso normal (de noche) se convierte en el escenario ideal de horror liminal (referencia directa Backrooms del GDD), reforzado por props de "abandono repentino" (silla volcada, herramientas de Rodrigo) que sugieren que algo interrumpió la normalidad sin aviso.

---

## 12. Optimización Godot 4

| Estrategia | Aplicación en este mapa |
|---|---|
| Sectores/Chunks | Dividir el andén en 3 sectores de ~18 m cada uno (Norte, Centro, Sur) como nodos `Node3D` independientes, permitiendo activar/desactivar procesamiento de detalle (props, luces dinámicas) fuera del sector activo del jugador |
| Occlusion Culling | Las columnas y la caseta de control son candidatas naturales a `OccluderInstance3D` — la geometría de la bóveda ya limita la visibilidad longitudinal, ideal para culling agresivo entre sectores |
| LOD | Props pequeños (basureros, extintores, cajas) con `VisualInstance3D` LOD a 2 niveles (detalle completo <15m, simplificado >15m) — dado el pasillo largo y recto, el LOD por distancia es muy efectivo aquí |
| Static Bodies | Piso, muros, bóveda, columnas y bordes de andén como `StaticBody3D` únicos por sector (no por instancia individual) para minimizar el número de cuerpos de física activos |
| Collision | Colisión simplificada (cajas) para toda la geometría arquitectónica; los fosos de vía (03/10) llevan un `Area3D` (no colisión sólida) usado solo para detectar si el jugador intenta bajar antes de tiempo (fuera del punto de descenso oficial) y bloquear/redirigir narrativamente |
| NavigationRegion3D | Una única región de navegación cubriendo el andén completo, usada exclusivamente para la IA de la entidad (según GDD, `entity_ai.gd` usa `NavigationAgent3D`) — el foso de vías se excluye de la malla de navegación en esta zona (la entidad no debe "flotar" sobre las vías aquí, eso es propio de la zona de túnel) |
| GridMap | Las columnas (9 instancias idénticas) y los segmentos de bóveda modular son candidatos ideales para `GridMap` con una malla de biblioteca reutilizable, reduciendo drásticamente el conteo de nodos en el árbol de escena |
| Instancing | Bancas, basureros, extintores, luminarias de cornisa: todos usan `MultiMeshInstance3D` o instancias de escena repetidas desde una única `PackedScene` base por tipo de prop |

---

## 13. Organización del proyecto

```
linea_cero/
├── assets/
│   ├── models/
│   │   └── anden_baquedano/
│   │       ├── columna_estructural.glb
│   │       ├── boveda_segmento.glb
│   │       ├── caseta_control.glb
│   │       ├── banca.glb
│   │       ├── basurero.glb
│   │       ├── panel_llegadas.glb
│   │       └── reja_bloqueo.glb
│   ├── textures/
│   │   ├── hormigon/              (reutilizado de Sala Técnica)
│   │   ├── metal_oxidado/         (reutilizado de Sala Técnica)
│   │   ├── terrazo_piso/
│   │   ├── ceramica_zocalo/
│   │   ├── franja_identificadora/
│   │   └── franja_tactil/
│   ├── materials/
│   │   └── anden_baquedano/       (.tres de cada material de la sección 7)
│   ├── audio/
│   │   └── anden_baquedano/
│   │       ├── zumbido_electrico.ogg
│   │       ├── chisporroteo_luz.ogg
│   │       ├── viento_tunel.ogg
│   │       ├── tren_fantasma.ogg
│   │       ├── radio_estatica.ogg
│   │       ├── pasos_terrazo.ogg
│   │       └── contacto_entidad_01.ogg
│   └── lights/
│       └── anden_baquedano_light_profiles.tres
├── scenes/
│   └── anden_baquedano/
│       ├── anden_baquedano.tscn          (escena raíz de la zona)
│       ├── sector_norte.tscn
│       ├── sector_centro.tscn
│       ├── sector_sur.tscn
│       └── props/
│           ├── panel_llegadas.tscn
│           └── caseta_control.tscn
├── scripts/
│   └── anden_baquedano/
│       ├── anden_baquedano.gd            (orquestador de zona: eventos, luces, audio)
│       ├── luz_fallo_secuencial.gd
│       ├── tren_fantasma_trigger.gd
│       └── panel_llegadas_interact.gd
└── design_docs/
    └── MAPA_AndenBaquedano.md            (este documento)
```

---

## 14. Checklist de producción (mínimo 100 puntos)

### Blockout (15)
- [ ] 1. Piso de andén modelado a escala real (7×55 m)
- [ ] 2. Muro norte cerrando el nivel
- [ ] 3. Muro sur con hueco oeste (boca de túnel transitable)
- [ ] 4. Muro sur con hueco este bloqueado (boca de túnel sellada)
- [ ] 5. Bóveda continua sin quiebres visibles
- [ ] 6. Foso de vía 1 modelado 1.1 m bajo andén
- [ ] 7. Foso de vía 2 modelado 1.1 m bajo andén
- [ ] 8. 9 columnas colocadas a 6 m de separación exacta
- [ ] 9. Volumen de caseta de control colocado junto a columna 05
- [ ] 10. Barreras de seguridad en los 4 extremos del andén
- [ ] 11. Reja de escalera norte bloqueando acceso
- [ ] 12. Reja de túnel este bloqueando acceso
- [ ] 13. Volumen de panel de llegadas suspendido correctamente
- [ ] 14. Punto de descenso a vía (BLOCK_Descenso_Via) accesible y alineado con boca oeste
- [ ] 15. Escala general verificada caminando con el player controller (sin proporciones "de juguete" ni "gigantes")

### Colisión y física (8)
- [ ] 16. Piso de andén con colisión sólida completa
- [ ] 17. Todos los muros con colisión sólida
- [ ] 18. Columnas con colisión individual (no atravesables)
- [ ] 19. Barreras de extremo con colisión (evitan caída accidental fuera del andén)
- [ ] 20. Foso de vía con `Area3D` de detección (no colisión sólida)
- [ ] 21. Punto de descenso a vía con lógica de transición de zona probada
- [ ] 22. Jugador no puede atravesar rejas de bloqueo
- [ ] 23. Jugador no queda atrapado en ninguna esquina o intersección de geometría

### Materiales y texturizado (12)
- [ ] 24. Material de piso terrazo aplicado con UV correcto (sin estiramiento)
- [ ] 25. Franja táctil amarilla alineada con el borde real del andén
- [ ] 26. Zócalo cerámico aplicado en muros bajos
- [ ] 27. Franja de color identificador aplicada en muros altos
- [ ] 28. Material de bóveda de hormigón sin artefactos de parallax (lección de Sala Técnica aplicada)
- [ ] 29. Columnas con material de hormigón pintado diferenciado del muro
- [ ] 30. Riel metálico con material de acero pulido
- [ ] 31. Durmientes con material de hormigón envejecido
- [ ] 32. Balasto con textura tileable sin repetición visible obvia
- [ ] 33. Rejas con material de metal oxidado (reutilizando Metal063)
- [ ] 34. Caseta de control con materiales mixtos correctamente asignados por submesh
- [ ] 35. Verificación de coherencia de color entre esta zona y Sala Técnica (misma "familia" de materiales reutilizados)

### Iluminación (14)
- [ ] 36. 9 luces de cornisa colocadas y alineadas a columnas
- [ ] 37. Sistema de fallo progresivo de luces implementado y probado (fase posterior, no en este documento)
- [ ] 38. Las luces que fallan nunca lo hacen por delante del jugador
- [ ] 39. 4 luces de emergencia rojas permanentes colocadas
- [ ] 40. Luces de emergencia nunca se apagan bajo ninguna condición
- [ ] 41. Luz emisiva del panel de llegadas configurada
- [ ] 42. Spotlight en boca de túnel oeste sugiriendo profundidad
- [ ] 43. Ambient light global configurado (sin negros absolutos)
- [ ] 44. Verificación de que la zona segura inicial (15 m) permanece siempre iluminada
- [ ] 45. Prueba de legibilidad: el jugador siempre puede ver dónde caminar, incluso con luces falladas
- [ ] 46. Sombras activadas solo en luces que lo requieren narrativamente (cornisa), desactivadas en emergencia
- [ ] 47. Balance de intensidad probado en build de Windows (no solo en editor)
- [ ] 48. Sin luces con `omni_range` excesivo generando "bleed" entre sectores
- [ ] 49. Temperatura de color consistente con la paleta general del GDD (cálido normal vs rojo emergencia vs frío túnel)

### Audio (13)
- [ ] 50. Zumbido eléctrico ambiente en loop configurado
- [ ] 51. Chisporroteo sincronizado a cada evento de fallo de luz
- [ ] 52. Viento de túnel con aumento de volumen por proximidad
- [ ] 53. Reverberación de espacio grande aplicada a todo el andén
- [ ] 54. Sonido de tren fantasma disparado por trigger de posición
- [ ] 55. Tren fantasma no se repite en el mismo punto exacto dos veces
- [ ] 56. Estática de radio vinculada a proximidad con la caseta de control
- [ ] 57. Voz de operador con frases cortadas implementada
- [ ] 58. Sonido de pasos limpio, sin anomalías (contraste con zona de túnel)
- [ ] 59. Evento único de "primer contacto auditivo con la entidad" configurado
- [ ] 60. Contacto auditivo con la entidad no se repite en la misma partida
- [ ] 61. Mezcla general de audio probada con auriculares y con parlantes
- [ ] 62. Ningún sonido ambiente compite en volumen con los eventos narrativos clave

### Props y set dressing (15)
- [ ] 63. 4 bancas colocadas a lo largo del andén
- [ ] 64. 3 basureros colocados
- [ ] 65. 2 extintores colocados junto a columnas
- [ ] 66. Caja de herramientas de Rodrigo colocada cerca del punto de descenso
- [ ] 67. Nota de técnico colocada sobre banca cercana a la caseta
- [ ] 68. Radio secundaria colocada dentro de la caseta y marcada como interactiva
- [ ] 69. Reloj de andén detenido en hora específica (detalle narrativo)
- [ ] 70. 3 carteles colgantes "BAQUEDANO" colocados
- [ ] 71. 9 placas de nombre en columnas colocadas
- [ ] 72. Señales "NO PASAR" en las 4 barreras de extremo
- [ ] 73. Señal "FUERA DE SERVICIO" en escalera norte
- [ ] 74. Señal "SIN SALIDA" en boca de túnel este
- [ ] 75. Panel de llegadas interactivo mostrando horario con trenes inexistentes (según GDD)
- [ ] 76. Silla de vigilante volcada colocada dentro/cerca de la caseta
- [ ] 77. Decals de humedad, óxido y basura dispersa aplicados sin saturar la escena

### Gameplay y triggers (10)
- [ ] 78. Spawn del jugador verificado en la posición y orientación correctas
- [ ] 79. Interacción con panel de llegadas funcional
- [ ] 80. Interacción con radio secundaria funcional
- [ ] 81. Nota de técnico legible e interactuable
- [ ] 82. Punto de no retorno (descenso a vía) probado en ambas direcciones (no se puede volver a subir)
- [ ] 83. Zona segura inicial confirmada sin eventos de tensión durante los primeros ~15 m
- [ ] 84. Secuencia completa jugada de principio a fin sin bloqueos ni softlocks
- [ ] 85. Ningún backtracking accidental posible (diseño lineal respetado)
- [ ] 86. Transición a zona 03 (Túnel km 1.4) probada y sin cortes visuales abruptos
- [ ] 87. Tiempo de recorrido real medido en playtesting, dentro del rango 5–15 min del GDD

### Optimización (12)
- [ ] 88. Mapa dividido en 3 sectores (Norte/Centro/Sur) como nodos independientes
- [ ] 89. Occlusion culling configurado usando columnas y caseta como occluders
- [ ] 90. LOD aplicado a props pequeños con umbral de 15 m
- [ ] 91. Static bodies consolidados por sector, no por instancia individual
- [ ] 92. Área de detección de foso de vía implementada como `Area3D`, no colisión sólida
- [ ] 93. NavigationRegion3D generado y probado con la IA de la entidad
- [ ] 94. Foso de vías excluido correctamente de la malla de navegación en esta zona
- [ ] 95. Columnas y segmentos de bóveda evaluados para migración a GridMap
- [ ] 96. Props repetidos (bancas, basureros, luminarias) usando instancias de escena, no meshes duplicados manualmente
- [ ] 97. FPS estable medido en hardware de referencia (mínimo objetivo, a definir por el equipo técnico)
- [ ] 98. Draw calls verificados con el profiler de Godot antes de aprobar la zona como "lista"
- [ ] 99. Memoria de texturas verificada (reutilización de Concrete034/Metal063 confirmada, sin duplicados)

### Narrativa y horror (6)
- [ ] 100. Simetría arquitectónica verificada como perfectamente repetitiva (sin variaciones accidentales que rompan el efecto liminal)
- [ ] 101. Curva de tensión confirmada: bajo→medio, sin picos prematuros
- [ ] 102. Ningún jump scare presente en ninguna iteración de prueba
- [ ] 103. Entidad confirmada como NUNCA visible en esta zona (solo auditiva)
- [ ] 104. Coherencia narrativa verificada con notas de lore de otras zonas (sin contradicciones no intencionales)
- [ ] 105. Playtesting con al menos 2 personas ajenas al desarrollo confirmando la sensación de "vacío inquietante" buscada

---

## 15. Adaptaciones de gameplay (justificación de desvíos respecto a la realidad)

| Desvío de la realidad | Justificación |
|---|---|
| Largo comprimido de ~100 m reales a 55 m jugables | Un recorrido de 100 m sin eventos intermedios generaría un ritmo muerto incompatible con la duración total de V1 (25–40 min para todo el juego). Se preserva la sensación de longitud mediante niebla y oscuridad en los extremos, no mediante metraje real |
| Boca de túnel este presente pero sellada (en la realidad ambas vías suelen ser funcionales) | Necesidad de diseño lineal sin ambigüedad de navegación — el GDD especifica "cuatro zonas lineales", por lo que ofrecer dos caminos reales rompería la estructura narrativa |
| Escaleras de acceso a mezzanine no modeladas en detalle, solo bloqueadas | Fuera del scope de V1 (25–40 min de juego total); modelar niveles superiores no aporta al objetivo narrativo y consume presupuesto de producción sin retorno de horror/gameplay |
| Color identificador de estación estimado (no verificado con fuente histórica exacta) | Documentado explícitamente como estimación; no afecta gameplay, solo estética — puede corregirse en Sem 5 (Assets y texturas) si se encuentra fuente fiable |
| Panel de llegadas LED (tecnología moderna) en una estación de diseño 1975 | Las estaciones de Metro Santiago fueron modernizadas con paneles LED reales en años posteriores — coherente con "estación actual", no rompe verosimilitud |

---

## 16. Errata de implementación (encontrada en Fase 3.3 — Materiales)

Al construir la colisión física en Godot se detectaron inconsistencias geométricas en el blockout original (sección 5) que fue necesario corregir. Documentadas aquí para que el plano superior (sección 3) se lea junto con esta errata:

| Elemento original | Problema detectado | Corrección aplicada |
|---|---|---|
| Muro Sur en dos piezas (Oeste/Este), cada una cubriendo el ancho de una vía | Bloqueaba físicamente el punto de descenso a la vía (11); geométricamente incorrecto: el andén termina en un muro, pero las vías **continúan** como túnel más allá de la estación en ambos sentidos, no terminan en un muro | Un único `Muro_Sur` de 7 m (solo el ancho del andén). Ambas vías quedan abiertas hacia el sur; el control de acceso se hace con la reja (12), no con un muro |
| Reja_Tunel_Este como muro completo (3.5×4×0.1) | No correspondía a un elemento realista — una vía sellada se bloquea con una reja a la altura del foso, no con un muro de altura completa | Reja reposicionada a la boca de la vía este, a la altura del foso (3.5×2.0×0.1 a y=-0.1) |
| Descenso_Via en x=-2 | Esa coordenada caía dentro del rango cubierto por el muro sur-oeste original (contradicción con su propia función) | Reposicionado a x=-3.75 (borde real andén/vía oeste), fuera del área de las barreras de esquina |
| Muros laterales largos (zócalo + franja identificadora) | **No existían en el blockout original** — sección 5 solo incluía los muros de cierre norte/sur, omitiendo las paredes largas que en la realidad llevan el elemento más reconocible de la identidad visual de Metro Santiago | Agregados: `Muro_Lateral_Oeste` y `Muro_Lateral_Este` en x=∓7, cada uno dividido en Zócalo (crema, 1.2 m) + Franja (ocre/mostaza, 3.1 m), recorriendo los 55 m completos |
| Bóveda como caja de blockout | Correcto para la fase de blockout (regla "solo cajas"), pero debía reemplazarse en la fase de Materiales/Detalle según lo ya previsto en la sección 5 | Reemplazada por un arco circular segmentado real (radio ≈21 m, alza 1.2 m sobre el arranque de 4.3 m → clave a 5.5 m), generado con `bmesh` en `generar_materiales.py` |

**Lección de proceso:** el blockout debe validarse con colisión física real (no solo revisión visual en el editor) antes de aprobar el paso a la fase de Materiales — varios de estos errores solo se manifestaron al intentar caminar sobre la geometría con el `CharacterBody3D` del jugador.

---

**FIN DEL DOCUMENTO — Fase 2 completa.**

Según el proceso solicitado, ahora corresponde **esperar aprobación** antes de iniciar la Fase 3 (Implementación en Godot: blockout → iluminación → materiales → props → audio → navegación → gameplay, en ese orden estricto, sin mezclar fases).
