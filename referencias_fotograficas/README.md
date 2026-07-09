# Referencias fotográficas — Estación Baquedano

**Objetivo:** recopilar 150–300 fotografías reales de la Estación Baquedano (Metro de Santiago, combinación Línea 1 ↔ Línea 5) para modelado 3D fiel en Blender/Godot.

**Estado:** 🟡 Investigación online inicial completa (esta sesión). Fotografía en persona **pendiente** — la mayoría de las categorías necesitan cobertura fotográfica real que no existe públicamente organizada como set completo.

---

## ⚠️ Corrección crítica respecto al diseño ya construido

La investigación confirma que **Baquedano NO es una estación de un solo andén de Línea 1** (como se documentó y construyó en `MAPA_AndenBaquedano.md` v1.0/v2.0). Es una **estación de combinación L1 ↔ L5** con:

- **6 niveles** totales (distribución norte-sur y este-oeste)
- **6 andenes/vías** en total — solo 4 operativos actualmente (L1 + L5), **2 reservados para la futura Línea 7**
- Andenes de **L1 y L5 a profundidades distintas** (L1 construida 1977 por tajo abierto/cut-and-cover; L5 construida 1997, totalmente subterránea/excavación profunda)
- Un **nivel de combinación** (hall de transferencia) que conecta ambas líneas, con ~200+ m² de muros ocupados por instalaciones de arte (MetroArte)
- **4 accesos de superficie** (A–D), uno con ascensor para accesibilidad
- **4 ascensores** totales (1 de acceso + 3 de transferencia interna L1↔L5)
- Servicios: máquinas de carga Bip!, oficina de atención, cajero automático, tienda Maxi-K, Bibliometro (biblioteca), múltiples exhibiciones de arte (MetroArte: "La Bajada", "El Santiaguillo", mural "Ágora" de 400 m² de Javier Godoy)
- **Sistema eléctrico:** 750V DC por riel guía (tercer riel), no catenaria aérea — consistente con nuestra señalética "PELIGRO ALTO VOLTAJE" ya implementada
- **Historia reciente relevante para el lore/horror:** acceso principal incendiado el 25 de octubre de 2019 (protestas sociales), reabierto parcialmente en 2020, reconstrucción completa de la "plaza hundida" de acceso terminada en enero 2024 (ahora es una explanada sin plaza hundida)

**Implicación para el proyecto:** lo construido hasta ahora (andén único de 100m, 17 columnas, sin hall ni L5 ni conexión) es efectivamente una **estación genérica de Línea 1 inspirada en Baquedano**, no una recreación fiel de Baquedano real. Para que sea fiel hay que agregar como mínimo: hall de combinación, andén L5 (a otra profundidad), pasillos de conexión, torniquetes, accesos A–D. Esto es un rediseño de alcance mayor — recomendado documentarlo como **Fase 1.5 / Zona 02b** antes de seguir con props de detalle.

---

## Fuentes oficiales encontradas (alta confiabilidad)

| Fuente | Contenido | URL |
|---|---|---|
| Metro de Santiago — página oficial L1 | Accesos, ascensores, servicios, horarios | https://www.metro.cl/el-viaje/estaciones/BA |
| Metro de Santiago — página oficial L5 | Info del lado L5 | https://www.metro.cl/estacion/BQ |
| Wikipedia ES — Baquedano (estación) | Historia técnica: 6 niveles, 6 andenes, construcción 1977/1997, incendio 2019, reapertura 2024 | https://es.wikipedia.org/wiki/Baquedano_(estaci%C3%B3n_del_Metro_de_Santiago) |
| Wikimedia Commons | **102 archivos** — la fuente más rica encontrada, ver desglose abajo | https://commons.wikimedia.org/wiki/Category:Baquedano_station |
| Wiki Metro de Santiago (Fandom) | Ficha técnica alternativa | https://metrodesantiago.fandom.com/es/wiki/Baquedano |
| T13 — reconstrucción acceso principal 2024 | Fotos del estado actual del acceso tras renovación (sin plaza hundida) | https://www.t13.cl/amp/noticia/nacional/se-acabo-plaza-hundida-asi-luce-nueva-renovada-salida-principal-baquedano-5-1-2024 |

## Desglose de Wikimedia Commons (102 archivos) por categoría del proyecto

| Carpeta del proyecto | Archivos identificados |
|---|---|
| `05_Linea1` | `Baquedano L1.jpg` |
| `06_Linea5` | `Baquedano L5.jpg`, `Andenes Estacion Baquedano L5.jpg` (3840×2160), `Estación Baquedano - andén L5 a Vicente Valdés.jpg` |
| `07_Combinacion` | `Baquedano nivel de combinación L1 y L5.jpg` ← **imagen clave, buscar primero** |
| `04_Pasillos` | Serie `Paseo borde Mapocho 2021 - Interior estación Baquedano (41-43).jpg` (3 fotos) |
| `01_Exterior` | Serie `Antigua salida de estación Baquedano (37-39).jpg` (histórica, pre-incendio), `Salida B de la estación Baquedano (31-33).jpg`, `Salida Baquedano, Providencia, Santiago 20240412.jpg` (2024, post-renovación) |
| `09_Senaletica` | Serie `Cenefa Metro Baquedano` (5 versiones a través de los años — útil para ver evolución del diseño de señalética/franja identificadora) |
| `11_Objetos` (arte) | Series de murales: Benmayor "Declaración de amor", Miranda "Ojo en azul" (7 fotos), Lorca "Rostros del Bicentenario" (12 fotos), Smythe "Vía Láctea" (8 fotos), Pinto "La bajada" (4 fotos) — no son props reutilizables pero sí referencia de cómo se integra arte a los muros |
| Contexto histórico | `Baquedano incendiado.jpg`, `Protestas en Chile 20191025 47.jpg` — relevante solo si se usan como Easter egg de lore, no para geometría base |

**Acción recomendada:** descargar directamente estos ~35-40 archivos identificados por nombre desde Commons (son de uso libre, licencia Wikimedia) antes de recurrir a fotografía en persona — cubren varias de las categorías base.

## Otras fuentes con material disperso (revisar manualmente)

- Flickr — Ignacio Paredes: álbum "METRO DE SANTIAGO" (colección amplia, sin confirmar cuántas de Baquedano específicamente) — https://www.flickr.com/photos/ignacioparedes/albums/72157627203517381/
- Flickr — La Biblioteca de Transportes: foto específica de andén L1 — https://www.flickr.com/photos/labibliotecadetransportes/20723283745
- Metro.cl noticias — mural "Ágora" (2018) con fotos del pasillo de acceso a andén — https://www.metro.cl/noticias/estacion-baquedano-renueva-su-imagen-con-nuevo-mural-dedicado-a-la-fotografia

## Categorías SIN cobertura online encontrada (requieren fotografía en persona obligatoriamente)

Estas categorías del checklist original no arrojaron resultados específicos de Baquedano en la búsqueda — no significa que no existan fotos, sino que no aparecieron en las 6 búsquedas realizadas en esta sesión:

- `02_Entorno` (calle, Plaza Italia a nivel de vereda, más allá de la fachada) — parcialmente cubierto por fuentes de Plaza Baquedano/Plaza Italia en general, no específico de los accesos del metro
- `03_Hall` (boletería, torniquetes específicamente en Baquedano) — 0 resultados directos
- `08_Escaleras` (mecánicas, descansos, barandas — específicas de Baquedano) — 0 resultados directos, aunque Wikipedia confirma "numerosas escaleras mecánicas y estándar"
- `10_Texturas` (fotos perpendiculares de piso/baldosa/hormigón para conversión a textura tileable) — este tipo de foto técnica casi nunca existe en bancos públicos, es intrínsecamente material de terreno
- `12_Iluminacion` (día/noche, sombras, reflejos) — no encontrado como set fotográfico

---

## Checklist para fotografía en persona (prioridad)

Usa esto como guía al visitar la estación. Prioridad alta = lo que más impacta la fidelidad del modelo y no se encontró online.

### 🔴 Prioridad alta (sin cobertura online)
1. **Hall de combinación completo** — ambos extremos, techo, piso, boleterías, torniquetes (`03_Hall`)
2. **Escaleras mecánicas y fijas** de conexión L1↔L5 — vista superior e inferior, barandas, descansos (`08_Escaleras`)
3. **Texturas perpendiculares** de piso, baldosa, hormigón, pintura, acero — foto de frente, sin ángulo, buena luz (`10_Texturas`)
4. **Accesos A, B, C, D** desde la calle, de día — el acceso principal ya se renovó en 2024, la Wikimedia solo tiene fotos viejas/incendiadas (`01_Exterior`)

### 🟡 Prioridad media (cobertura parcial online)
5. Andén L5 completo, ambos sentidos (Vicente Valdés confirmado, falta sentido contrario) (`06_Linea5`)
6. Pasillos largos, curvas, cruces (solo 3 fotos de interior encontradas) (`04_Pasillos`)
7. Objetos: basureros, validadores, cámaras, parlantes, relojes, extintores (`11_Objetos`)
8. Iluminación día/noche, andenes vacíos (`12_Iluminacion`)

### 🟢 Prioridad baja (buena cobertura ya encontrada)
9. Andén L1 (imagen confirmada, complementar con más ángulos)
10. Nivel de combinación (imagen clave ya identificada)
11. Señalética / cenefa (5 versiones históricas ya en Commons)
12. Entorno / Plaza Italia (abundante material general, aunque no específico del acceso metro)

---

## Estructura de carpetas

```
referencias_fotograficas/
├── 01_Exterior/
├── 02_Entorno/
├── 03_Hall/
├── 04_Pasillos/
├── 05_Linea1/
├── 06_Linea5/
├── 07_Combinacion/
├── 08_Escaleras/
├── 09_Senaletica/
├── 10_Texturas/
├── 11_Objetos/
└── 12_Iluminacion/
```

Al fotografiar o descargar, guardar directamente en la subcarpeta correspondiente con nombre descriptivo (ej. `07_Combinacion/nivel_transferencia_vista_norte_01.jpg`).
