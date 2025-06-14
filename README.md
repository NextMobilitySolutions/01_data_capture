# **Documentación Técnica – Módulo de Captura de Datos para HUD Inteligente**

## **Descripción General**

Este repositorio contiene los scripts necesarios para la recopilación y subida de datos visuales (imágenes en formato comprimido `.zip`) a Google Cloud Storage, con el objetivo de alimentar un sistema de entrenamiento de modelos de visión por computador en el contexto de un Head-Up Display (HUD) para vehículos. El módulo está diseñado para admitir archivos provenientes de múltiples fuentes: vehículos reales, simuladores y datasets abiertos.

## **Estructura del Repositorio**

```bash
01_DATA_CAPTURE/
├── data/                           # Carpeta para colocar archivos ZIP con imágenes
│   └── xxxxxx.zip
├── help/                           # Scripts y recursos de apoyo
│   ├── culane_segmentations.py     # Script de segmentación del dataset CULane
│   └── youtube_frame_extractor.py  # Script para extraer frames desde vídeos de YouTube
├── src/
│   ├── config.py                   # Carga de configuraciones desde .env
│   └── uploader.py                 # Subida directa de imágenes desde ZIP a GCS
├── main.py                         # Script principal para ejecutar el flujo de subida
├── .env                            # Archivo de variables de entorno
├── .gitignore                      # Exclusiones para entorno y archivos temporales
├── LICENSE
└── README.md
```

## **Requisitos Técnicos**

* Python 3.8 o superior
* Acceso a un proyecto de Google Cloud Platform con permisos sobre Google Cloud Storage
* Archivo `.env` configurado correctamente

## **Instalación y Entorno**

### **Entorno Virtual**

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### **Instalación de Dependencias**

```bash
pip install -r requirements.txt
```

## **Configuración del Entorno**

Crear un archivo `.env` con el siguiente contenido:

```bash
PROJECT_ID=nombre-del-proyecto-gcp
BUCKET_NAME=nombre-del-bucket
TARGET_ROOT_PATH=carpeta/en/gcs
DEFAULT_ZIP_PATH=data/xxxxxx.zip
```

## **Ejecución del Script**

### **Subida estándar (configuración por defecto)**

```bash
python main.py
```

### **Subida personalizada (argumentos CLI)**

```bash
python main.py --zip data/xxxxxx.zip --target raw/simulador/escenario_1
```

## **Arquitectura Interna del Módulo**

* `main.py`: Orquesta la ejecución tomando los argumentos de entrada o las variables por defecto del entorno.
* `config.py`: Carga las variables desde `.env` y valida las necesarias.
* `uploader.py`: Carga el archivo `.zip` en memoria, detecta imágenes válidas y las sube directamente al bucket de GCS sin necesidad de descomprimir localmente.

## **Organización de Datos en GCS**

```bash
raw/
├── public/
│   ├── bdd100k/
│   ├── culane/
│   ├── acdc/
│   ├── lisa/
│   ├── youtube/
├── simulated/
│   └── carla/
└── real/
```

## **Fuentes de Datos Utilizadas**

Además de los datasets públicos y simulados, se han incorporado imágenes adicionales extraídas manualmente a partir de vídeos de YouTube. Estas imágenes permiten cubrir escenarios no disponibles en datasets tradicionales, como carreteras en mal estado, caminos rurales sin líneas de demarcación y entornos de visibilidad compleja. Se han generado conjuntos personalizados en la ruta `raw/public/youtube/` con los siguientes vídeos:

* dirtroad_night_forest/ — [YouTube](https://www.youtube.com/watch?v=zHh_XXBsvqw)
* rural_day_villages/ — [YouTube](https://www.youtube.com/watch?v=ScJaThvSa6E)
* dirtroad_day_bumpy_2018/ — [YouTube](https://www.youtube.com/watch?v=-unCk3FOIXU)
* dirtroad_bumpy/ — [YouTube](https://www.youtube.com/watch?v=A9ly_2P5bO0&t=580s)
* rural_day_villages_2/ — [YouTube](https://www.youtube.com/watch?v=ZUWpXIXgeYg)
* dirtroad_night_forest_2/ — [YouTube](https://www.youtube.com/watch?v=_xlvk-w9tiE)

### **Descripción de los Datasets**

* **BDD100K (10K)**: Imágenes urbanas anotadas para detección y segmentación. Dividido en `train`, `val`, `test`.
* **CULane**: Imágenes centradas en detección de carriles bajo distintas condiciones (`normal`, `shadow`, etc.).
* **ACDC**: Escenarios urbanos adversos (`fog`, `night`, `rain`, `snow`).
* **LISA Traffic Light**: Detección de semáforos bajo condiciones de luz `day` y `night`.
* **CARLA**: Datos sintéticos generados mediante simulación, organizados en `train` y `val`.

## **Resumen Tabular de Conjuntos**

| Origen             | Descripción                                                      | Ruta destino en GCS    | Estado    | Imágenes | Tamaño Aprox. |
| ------------------ | ---------------------------------------------------------------- | ---------------------- | --------- | -------- | ------------- |
| BDD100K (10K)      | Dataset urbano dividido en `train`, `val`, `test`.               | `raw/public/bdd100k/`  | Activo    | 10,004   | 3.14 GB       |
| CULane             | Frames con anotaciones por escenario (`normal`, `shadow`, etc.). | `raw/public/culane/`   | Parcial   | 2,046    | 1.9 GB        |
| ACDC               | Imágenes bajo condiciones climáticas adversas.                   | `raw/public/acdc/`     | Activo   | 4,007  | 28 GB         |
| LISA Traffic Light | Semáforos capturados en horario diurno y nocturno.               | `raw/public/lisa/`     | Parcial   | 11,390   | 3.93 GB       |
| CARLA Simulator    | Imágenes simuladas de entrenamiento y validación.                | `raw/simulated/carla/` | Parcial   | 1,865    | 0.14 GB       |
| YouTube Extracted  | Caminos rurales y sin demarcación extraídos de vídeos.           | `raw/public/youtube/`  | Parcial   |   9,857      | 5.97 GB             |
| Vehículo real      | Capturas reales aún pendientes de procesamiento.                 | `raw/real/`            | Pendiente | —        | —             |

> **Nota sobre la columna "Estado":**
> Esta columna indica el nivel de integración actual de cada dataset en el sistema:
>
> * **Activo**: el dataset ha sido completamente integrado, estructurado y se utiliza de forma habitual en los procesos de entrenamiento y validación: `train/val/test`.
> * **Parcial**: se han utilizado solo algunos subconjuntos.
> * **Pendiente**: el dataset ha sido identificado pero aún no ha sido procesado ni incorporado al pipeline de trabajo.

## **Referencias Externas**

* [BDD100K](http://bdd-data.berkeley.edu/download.html)
* [CULane](https://xingangpan.github.io/projects/CULane.html)
* [ACDC](https://acdc.vision.ee.ethz.ch/)
* [LISA Traffic Light](https://datasetninja.com/lisa-traffic-light)
* [CARLA Dataset](https://www.kaggle.com/datasets/alechantson/carladataset)

## **Consideraciones Técnicas**

* Solo se suben archivos con extensión `.jpg`, `.jpeg` o `.png`.
* Las rutas dentro del ZIP se aplanan para evitar estructuras de carpetas internas complejas.
* Las subidas se realizan de forma secuencial. Para procesamiento en paralelo, se recomienda adaptar `uploader.py` utilizando `concurrent.futures` o `asyncio`.

## **Medidas de Seguridad**

* No se deben subir archivos sensibles ni datos personales sin anonimizar.
* El archivo `.env` está incluido en `.gitignore` para evitar su exposición.

## **Licencia**

Este proyecto está licenciado bajo los términos definidos en el archivo `LICENSE` adjunto.
