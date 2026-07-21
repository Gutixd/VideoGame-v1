# MAPA_PlazaMaipu.md

**Proyecto:** LÍNEA CERO
**Zona:** 05 — Estación Plaza de Maipú (Línea 5)
**Autor:** Senior Level Designer / Environment Artist
**Estado:** 🟢 Aprobado para Implementación
**Versión:** 1.0

---

## 0. Fuente de investigación (Fase 1)

Basado en fuentes públicas y arquitectónicas reales de la estación terminal **Plaza de Maipú** de la Línea 5 del Metro de Santiago (inaugurada en 2011):

- **Arquitectura Urbana (Mobil Arquitectos / TRI Arquitectura):** Destaca por una gran trinchera abierta o explanada hundida que conecta la superficie (Plaza de Armas de Maipú) directamente con el nivel de boleterías, permitiendo iluminación y ventilación natural en niveles superiores.
- **Distribución de Andenes:** Configuración de **andén central (andén de isla)** con dos vías a los costados.
- **Profundidad:** Es una de las estaciones más profundas de la red, alcanzando los **22.7 metros** reales bajo la superficie.
- **Estética:** Estructura moderna de hormigón visto, vigas masivas de acero y hormigón cruzando las aberturas de luz, cielos planos panelados metálicos, y señalética característica de la Línea 5 (color verde).

---

## 1. Información general

| Campo | Valor |
|---|---|
| Nombre | Estación Plaza de Maipú |
| Zona (GDD) | 05 — Estación Plaza de Maipú |
| Objetivo narrativo | Mostrar una estación de diseño moderno y gran amplitud espacial completamente desierta. La escala monumental de las vigas y la explanada acentúan la soledad del jugador. La presencia de las colas de maniobras (túnel oscuro donde dan la vuelta los trenes) aporta misterio y peligro. |
| Objetivo del jugador | Entrar por la explanada de la superficie, cruzar los torniquetes inactivos de la mezzanine, descender a través de los descansos intermedios hasta el andén central, e investigar la caseta de control al final del andén. |
| Duración estimada | 5–10 min |
| Nivel de tensión | Bajo → Medio |
| Inspiración | Estructuras brutalisas modernas, espacios liminales subterráneos iluminados por luz de luna y focos de emergencia. |

---

## 2. Medidas

| Elemento | Medida real estimada | Medida usada en el nivel | Justificación |
|---|---|---|---|
| Explanada / Plaza Hundida | ~15 × 15 m | **15 × 15 m** | Fiel a la escala de acceso público. |
| Mezzanine (Largo × Ancho) | ~30 × 25 m | **30 × 25 m** | Espacio amplio para boleterías y torniquetes. |
| Altura de Mezzanine | ~4.5 m | **4.5 m** | Consistente con el diseño abierto de la estación. |
| Altura del Andén Central | ~5.0 m | **5.0 m** | Espacio alto bajo bóveda panelada moderna. |
| Ancho del Andén de Isla | ~8.0 m | **8.0 m** | Andén central ancho compartido por ambas vías. |
| Profundidad Total Relativa | ~22.7 m | **22.0 m** (desde Superficie Y=10 a Andén Y=-12) | Representación fiel de la profundidad. |
| Largo del Andén Modelado | ~120 m | **60 m** | Alcance de blockout para jugabilidad sin redundancia. |
| Escala del proyecto | 1 unidad Godot = 1 metro | — | Estándar del proyecto |

---

## 3. Plano superior (planta técnica)

```
NIVEL SUPERFICIE (Y = 10)
┌─────────────────────────────────┐
│     PLAZA DE ARMAS DE MAIPÚ     │
│  ┌───────────────────────────┐  │
│  │   EXPLANADA / CORTE (01)  │  │
│  │  ┌─────────────────────┐  │  │
│  │  │ Escaleras Bajada    │  │  │
│  └──┴─────────────────────┴──┘  │
└─────────────────────────────────┘
                │
                ▼
NIVEL MEZZANINE / BOLETERÍA (Y = 0)
┌────────────────────────────────────────────────────────┐
│                                                        │
│   02 (Boleterías)              03 (Oficinas Técnicas)  │
│                                                        │
│   ───────[ Torniquetes Inactivos (04) ]─────────       │
│                                                        │
│   05 (Espacio de Circulación Abierto)                  │
│                                                        │
│         [ Escalera Tramo 1 (06) a Nivel -6 ]           │
└────────────────────────────────────────────────────────┘
                │
                ▼
NIVEL INTERMEDIO DE TRANSICIÓN (Y = -6)
┌────────────────────────────────────────────────────────┐
│                                                        │
│               07 (Descanso Intermedio)                 │
│                                                        │
│         [ Escalera Tramo 2 (08) a Nivel -12 ]          │
└────────────────────────────────────────────────────────┘
                │
                ▼
NIVEL ANDÉN CENTRAL / ISLA (Y = -12)
┌────────────────────────────────────────────────────────┐
│ ░░░░░░░░░░░░░ VÍA 1 (Lado Oeste - Foso) ░░░░░░░░░░░░░  │
├─────┬────────────────────────────────────────────┬─────┤
│ 09  │                                            │ 11  │
│(Reja│  ANDÉN CENTRAL - ISLA (10)                 │(Sala│
│Cola)│                                            │Téc) │
├─────┼────────────────────────────────────────────┼─────┤
│ ░░░░░░░░░░░░░ VÍA 2 (Lado Este - Foso) ░░░░░░░░░░░░░  │
└────────────────────────────────────────────────────────┘
```

### Leyenda numerada

| # | Elemento | Descripción |
|---|---|---|
| 01 | Explanada Hundida | Foso abierto en el centro de la plaza que permite ver el cielo y el nivel mezzanine. |
| 02 | Boleterías | Caseta de vidrio y acero para la venta de boletos (vacía y sin luz). |
| 03 | Oficinas Técnicas | Muros ciegos metálicos que contienen salas de transformadores y sistemas. |
| 04 | Fila de Torniquetes | 6 torniquetes de acero inoxidable alineados, apagados y desbloqueados. |
| 05 | Circulación Mezzanine | Área amplia tras torniquetes con barandas metálicas que miran al nivel intermedio. |
| 06 | Escalera Tramo 1 | Rampa de escaleras mecánicas y fijas detenidas desde Y=0 a Y=-6. |
| 07 | Descanso Intermedio | Plataforma intermedia de distribución con muros de hormigón. |
| 08 | Escalera Tramo 2 | Escalera de bajada final desde Y=-6 a Y=-12 que llega al centro del andén. |
| 09 | Reja Cola de Maniobras | Límite norte del andén. Reja cerrada que da paso al túnel oscuro de maniobras. |
| 10 | Andén Central | Plataforma de embarque rodeada por las vías, con columnas centrales de sección circular. |
| 11 | Sala de Control Andén | Caseta técnica al extremo sur del andén con pantallas CRT apagadas. |

---

## 4. Vista isométrica (descripción)

El nivel de Plaza de Maipú se caracteriza por su verticalidad e iluminación de claroscuro. Al entrar por la superficie a través de la explanada a nivel de calle (Y=10), el jugador desciende por amplias escaleras sintiendo cómo se sumerge en la tierra. 

- **Contraste de Altura:** El nivel mezzanine tiene un vacío central donde las escaleras bajan al andén, permitiendo ver los andenes a 12 metros de profundidad desde arriba.
- **Vigas Cruzadas:** Gigantescas vigas de hormigón visto cruzan de lado a lado la trinchera abierta, proyectando sombras alargadas bajo la luz de la luna o de los pocos focos activos.
- **Techo del Andén:** A diferencia del andén abovedado clásico de Baquedano, el andén de Plaza de Maipú posee un cielo plano compuesto por paneles metálicos suspendidos de color gris oscuro, con canaletas para luminarias fluorescentes empotradas de luz fría.

---

## 5. Blockout (coordenadas para el script)

El origen local (0,0,0) corresponde al centro del piso de la Mezzanine. 
Eje **X** = Este / Oeste
Eje **Y** = Altura (Up)
Eje **Z** = Norte / Sur

| Nombre | Tipo | Posición (X, Y, Z) | Escala (Ancho × Alto × Largo) | Descripción |
|---|---|---|---|---|
| `BLOCK_Plaza_Calle` | Box | (0.0, 10.0, -25.0) | (20.0, 0.2, 20.0) | Nivel de superficie exterior (calle) |
| `BLOCK_Escalera_Calle` | Box | (0.0, 5.0, -12.5) | (6.0, 10.0, 5.0) | Escalera que conecta calle con la explanada |
| `BLOCK_Piso_Explanada` | Box | (0.0, 0.0, -5.0) | (16.0, 0.2, 10.0) | Piso de la explanada abierta inferior |
| `BLOCK_Piso_Mezzanine` | Box | (0.0, 0.0, 12.5) | (30.0, 0.2, 25.0) | Piso de la zona cerrada de mezzanine |
| `BLOCK_Techo_Mezzanine` | Box | (0.0, 4.5, 12.5) | (30.0, 0.2, 25.0) | Techo de la Mezzanine |
| `BLOCK_Muro_Oeste_Mezz` | Box | (-15.0, 2.25, 12.5) | (0.5, 4.5, 25.0) | Muro lateral oeste |
| `BLOCK_Muro_Este_Mezz` | Box | (15.0, 2.25, 12.5) | (0.5, 4.5, 25.0) | Muro lateral este |
| `BLOCK_Muro_Sur_Mezz` | Box | (0.0, 2.25, 25.0) | (30.0, 4.5, 0.5) | Muro de fondo sur |
| `BLOCK_Viga_Estructural_01`| Box | (0.0, 4.5, -5.0) | (16.0, 1.2, 1.5) | Viga de hormigón en la zona abierta |
| `BLOCK_Boleteria` | Box | (-10.0, 1.1, 8.0) | (3.0, 2.2, 4.0) | Caseta de boletería en mezzanine |
| `BLOCK_Torniquetes` | Box | (0.0, 0.5, 12.0) | (12.0, 1.0, 0.8) | Barrera de torniquetes (volumen simplificado) |
| `BLOCK_Escalera_Tramo1` | Box | (0.0, -3.0, 20.0) | (5.0, 6.0, 8.0) | Escalera desde Mezzanine (Y=0) a Nivel -6 |
| `BLOCK_Descanso_Intermedio`| Box | (0.0, -6.0, 27.0) | (8.0, 0.2, 6.0) | Piso del descanso intermedio |
| `BLOCK_Escalera_Tramo2` | Box | (0.0, -9.0, 33.0) | (5.0, 6.0, 6.0) | Escalera desde Descanso (Y=-6) a Andén (Y=-12) |
| `BLOCK_Piso_Anden` | Box | (0.0, -12.0, 60.0) | (8.0, 0.2, 60.0) | Andén de isla central (Y=-12) |
| `BLOCK_Foso_Via_Oeste` | Box | (-5.75, -13.1, 60.0) | (3.5, 2.0, 65.0) | Vía 1 (Foso izquierdo) |
| `BLOCK_Foso_Via_Este` | Box | (5.75, -13.1, 60.0) | (3.5, 2.0, 65.0) | Vía 2 (Foso derecho) |
| `BLOCK_Muro_Oeste_Anden` | Box | (-7.5, -9.0, 60.0) | (0.5, 6.0, 60.0) | Muro lateral del túnel de andén (oeste) |
| `BLOCK_Muro_Este_Anden` | Box | (7.5, -9.0, 60.0) | (0.5, 6.0, 60.0) | Muro lateral del túnel de andén (este) |
| `BLOCK_Techo_Anden` | Box | (0.0, -6.0, 60.0) | (15.5, 0.2, 60.0) | Techo panelado del andén |
| `BLOCK_Sala_Control` | Box | (0.0, -10.5, 85.0) | (4.0, 3.0, 4.0) | Caseta de control al extremo sur del andén |
| `BLOCK_Reja_ColaManiobras` | Box | (0.0, -10.5, 30.5) | (8.0, 3.0, 0.1) | Cierre de seguridad hacia cola de maniobras |
| `BLOCK_Columna_Anden_01` | Cylinder | (0.0, -9.0, 45.0) | (0.8, 6.0, 0.8) | Columna de soporte estructural |
| `BLOCK_Columna_Anden_02` | Cylinder | (0.0, -9.0, 55.0) | (0.8, 6.0, 0.8) | Columna de soporte estructural |
| `BLOCK_Columna_Anden_03` | Cylinder | (0.0, -9.0, 65.0) | (0.8, 6.0, 0.8) | Columna de soporte estructural |
| `BLOCK_Columna_Anden_04` | Cylinder | (0.0, -9.0, 75.0) | (0.8, 6.0, 0.8) | Columna de soporte estructural |

---

## 6. Materiales y Estética

| Elemento | Color base | Material | Roughness | Metallic |
|---|---|---|---|---|
| Muros de Hormigón | Gris neutro medio (0.45, 0.45, 0.47) | Hormigón pulido / bruto | 0.5 | 0.0 |
| Vigas Estructurales | Gris acero oscuro (0.2, 0.2, 0.22) | Acero / Hormigón armado | 0.3 | 0.4 |
| Techo Panelado | Gris oscuro panel (0.15, 0.15, 0.17) | Aluminio anodizado | 0.4 | 0.5 |
| Piso Mezzanine/Andén | Gris claro granulado (0.7, 0.7, 0.72) | Baldosas antideslizantes | 0.3 | 0.0 |
| Torniquetes / Rejas | Metal pulido (0.75, 0.75, 0.77) | Acero inoxidable | 0.2 | 0.8 |

---

## 7. Iluminación

- **Luz de Luna (Exteriores):** Foco tipo `DirectionalLight3D` cenital simulando la noche, filtrándose a través de la explanada hundida (`BLOCK_Piso_Explanada`). Color azul oscuro/grisáceo.
- **Iluminación Mezzanine:** Luces empotradas en los bordes del muro. En su mayoría apagadas, con algunas parpadeando sutilmente.
- **Iluminación del Andén Central:** Luces fluorescentes tubulares en el centro del techo (`Techo_Anden`). Emiten una luz fría y pálida ($Color = [0.85, 0.9, 1.0]$), concentrada en la zona central del andén, dejando las vías y los muros laterales sumidos en la penumbra.
- **Señalética Verde:** Luces autoluminosas débiles en los letreros de dirección ("Plaza de Maipú / Vicente Valdés") para orientar al jugador.

---

## 8. Sonidos Atmosféricos

- **Eco de Gran Altura:** Reverberación amplia característica de un espacio semiabierto de gran profundidad.
- **Viento Subterráneo Leve:** Sonido sutil de aire corriendo desde la cola de maniobras hacia la explanada.
- **Parpadeo de Neon:** Sonido eléctrico de alta frecuencia cerca de las luces que fallan.
