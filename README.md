## Rotten Tomatoes Movies – EDA

### 1) Objetivo
Analizar 16 638 películas del catálogo de Rotten Tomatoes para entender la relación entre la puntuación de la crítica (Tomatometer) y la puntuación del público, identificar géneros y clasificaciones predominantes, y detectar sesgos sistemáticos entre ambas audiencias.

### 2) Dataset
- **Fuente:** [Rotten Tomatoes Movies – Kaggle](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews)
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
- Q2: ¿Las películas *Certified Fresh* también reciben mejores puntuaciones del público?
- Q3: ¿Qué géneros predominan en el catálogo?
- Q4: ¿En qué películas el público y la crítica discrepan más?
- Q5: ¿Cómo se relacionan el Tomatometer y la puntuación del público globalmente?

### 3.1) Respuestas a Q1–Q5
- **Q1 (distribución Tomatometer):** Hay sesgo hacia puntuaciones altas; no se observa una bimodalidad clara. La masa principal se concentra en valores medios-altos/altos, con una cola hacia puntuaciones bajas.
- **Q2 (Certified Fresh y público):** En promedio, *Certified Fresh* presenta mejores puntuaciones de público que *Fresh* y *Rotten*, aunque con mayor dispersión.
- **Q3 (géneros predominantes):** Predominan **Drama** y **Comedia**, seguidos por **Action** y **Thriller** (ver top de géneros).
- **Q4 (mayor discrepancia público vs crítica):** La discrepancia se mide con `audience_vs_critics = audience_rating - tomatometer_rating`. En el notebook se incluye una tabla con el top de películas donde más gana el público y donde más gana la crítica.
- **Q5 (relación global crítica-público):** Existe correlación positiva moderada: cuando sube el Tomatometer, suele subir Audience, pero con dispersión relevante en los extremos.

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
- **El Tomatometer está sesgado hacia puntuaciones altas**: no hay una bimodalidad clara; esta conclusión se apoya en el cálculo mostrado en el notebook (media ≈ 60.45, mediana = 66, 34.7 % de películas con 80+ y 26.2 % por debajo de 40).
- **Los críticos puntúan ligeramente más alto que el público**: en el 54 % de las películas `tomatometer_rating > audience_rating` (mediana del gap = −2 pp). La media (~0) es engañosa por los valores extremos de la cola positiva.
- **Drama y Comedia dominan el catálogo**, seguidos de Acción y Thriller.
- **Las películas *Certified Fresh* sí reciben mejor puntuación del público**, pero con mayor varianza que las *Fresh*.
- **R y NR son los ratings MPAA más frecuentes** (>60 % del catálogo combinados).

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
