## Rotten Tomatoes Movies – EDA

### 1) Objetivo
Analizar 16 638 películas del catálogo de Rotten Tomatoes para entender la relación entre la puntuación de la crítica (Tomatometer) y la puntuación del público, identificar géneros y clasificaciones predominantes, y detectar sesgos sistemáticos entre ambas audiencias.

### 2) Dataset
- **Fuente:** [Rotten Tomatoes Movies ](https://mavenanalytics.io/data-playground/movie-ratings)
- **Archivo:** `data/raw/Rotten Tomatoes Movies.csv`
- **Nº filas / columnas:** 16 638 × 17
- **Variables clave:** `tomatometer_rating`, `audience_rating`, `tomatometer_status`, `rating` (MPAA), `genre`, `runtime_in_minutes`, `in_theaters_date`

**Glosario rápido de `rating` (MPAA):**
- `G`: público general.
- `PG`: se sugiere guía parental.
- `PG-13`: contenido potencialmente no apto para menores de 13 sin supervisión.
- `R`: menores de 17 acompañados por adulto.
- `NC17`: solo adultos (17+).
- `NR`: no clasificada oficialmente.

### 3) Preguntas de investigación
- Q1: ¿Cómo se distribuye el Tomatometer Rating? ¿Existe sesgo hacia valoraciones extremas?
- Q2: ¿Las películas *Certified Fresh* reciben mejor valoración del público que *Fresh* y *Rotten*, y con qué magnitud?
- Q3: ¿Qué géneros están mejor valorados por el público y cuáles concentran mayor visualización por película (métrica proporcional)?
- Q4: ¿Dónde se concentra el desacuerdo público-crítica: en patrones por género y en casos extremos individuales?
- Q5: ¿Cómo se relacionan el Tomatometer y la puntuación del público globalmente?
- Q6: ¿Cuál es la tendencia temporal del visionado típico por película y por qué conviene usar la mediana en lugar de la media?

### 3.1) Respuestas a Q1–Q6
- **Q1 (distribución Tomatometer):** La distribución presenta sesgo hacia puntuaciones altas y no muestra bimodalidad clara. En el dataset limpio, la media es **60.45** y la mediana **66**; el **34.66 %** de películas está en 80+ y el **26.17 %** por debajo de 40.
- **Q2 (Certified Fresh y público):** Sí. La media de `audience_rating` por status es **76.99** (*Certified Fresh*), **68.07** (*Fresh*) y **47.02** (*Rotten*), lo que confirma una diferencia sustancial a favor de *Certified Fresh*.
- **Q3 (géneros mejor valorados y más visualizados en proporción):**
    - Por valoración del público (media de `audience_rating`, n >= 50), destacan **Documentary (73.84)** y **Classics (72.06)**.
    - Por visualización proporcional (`audience_count` medio por película, n >= 50), lideran **Animation (421,474)**, **Action & Adventure (272,592)** y **Comedy (257,556)**.
- **Q4 (desacuerdo público vs crítica):** La discrepancia se define como `audience_vs_critics = audience_rating - tomatometer_rating`. A nivel global, el patrón favorece ligeramente a la crítica (mediana **-2** y **54.10 %** de películas con `tomatometer_rating > audience_rating`). Además, el desacuerdo se concentra en segmentos específicos por género (p. ej., **Comedy +3** vs **Classics -9**) y en una cola de casos extremos individuales.
- **Q5 (relación global crítica-público):** Se observa una correlación positiva moderada-alta (**corr = 0.6615**): cuando aumenta el Tomatometer, tiende a aumentar la puntuación del público, aunque persiste dispersión relevante y desacuerdos puntuales.
- **Q6 (tendencia temporal del visionado típico):** La mediana anual de `audience_count` muestra una evolución más estable que la media, con niveles altos en los 90/2000 y una caída marcada en la década de 2010. Es la métrica recomendada para comparar años porque reduce la distorsión causada por blockbusters extremos.

### 4) Data issues & fixes
| Problema | Solución (`src/cleaning.py`) |
|---|---|
| Typos en `rating` (`PG-13)`, `R)`) | `str.replace(')', '')` |
| `tomatometer_status` sin typos de formato | Se validan valores esperados: `Rotten`, `Fresh`, `Certified Fresh` |
| 1 fila duplicada exacta | `drop_duplicates()` |
| 8 329 nulos en `critics_consensus` | Rellenar con `'No consensus'` |
| 155 nulos en `runtime_in_minutes` | `dropna(subset=[...])` |
| Fechas como string | `pd.to_datetime(..., errors='coerce')` |
| `tomatometer_status` sin orden | `pd.Categorical(..., ordered=True)` |

### 5) Pipeline
```
data/raw/Rotten Tomatoes Movies.csv
    → src/io.py       load_csv()
    → src/cleaning.py clean()          # tipos, nulos, duplicados, categorías
    → src/features.py build_features() # theater_year, audience_vs_critics, primary_genre
    → src/viz.py      plot_graph()     # 6 visualizaciones
    → data/processed/clean_dataset.csv
```

### 6) Hallazgos principales
- **Tomatometer sesgado a notas altas**: no aparece bimodalidad clara; media **60.45**, mediana **66**, con **34.66 %** de películas en 80+ y **26.17 %** por debajo de 40.
- **Crítica ligeramente más generosa que el público**: en **54.10 %** de películas se cumple `tomatometer_rating > audience_rating`; la mediana de `audience_vs_critics` es **−2**.
- **Desacuerdo público-crítica heterogéneo por género**: la mediana del gap cambia de forma relevante entre géneros (ejemplos: **Comedy +3** vs **Classics −9**), además de existir una cola de casos extremos individuales.
- **Certified Fresh destaca también en público**: `audience_rating` medio **76.99** frente a **68.07** (*Fresh*) y **47.02** (*Rotten*).
- **Popularidad por género: usar métrica proporcional**: por `audience_count` medio por película (n >= 50) lideran **Animation (421,474)**, **Action & Adventure (272,592)** y **Comedy (257,556)**.
- **Picos 2003-2005 explicados por outliers**: la media anual de `audience_count` se dispara por blockbusters; el top 5 concentra **56.2 %** (2003), **49.7 %** (2004) y **38.9 %** (2005) del total anual.
- **Tendencia temporal robusta con mediana**: la mediana anual describe mejor la película “típica”; en años recientes cae con fuerza (ej.: **25,377** en 2006 vs **124** en 2019), evitando la distorsión de la media por títulos extremos.

### 7) Estructura del proyecto
```
project_demo/
├── main.py                # Entrypoint reproducible
├── data/
│   ├── raw/               # CSV original (no modificar)
│   └── processed/         # clean_dataset.csv + eda_visualizations.png
├── notebooks/
│   └── eda.ipynb          # EDA narrativo y orquestado
├── src/
│   ├── config.py          # Rutas RAW_PATH / OUT_PATH
│   ├── io.py              # load_csv()
│   ├── cleaning.py        # clean()
│   ├── features.py        # build_features()
│   ├── viz.py             # plot_graph()
│   └── utils.py           # assert_columns()
├── README.md
└── requirements.txt
```

### 8) Cómo ejecutar
```bash
pip install -r requirements.txt
python main.py                  # pipeline completo → data/processed/
# o abrir y ejecutar: notebooks/eda.ipynb
```
