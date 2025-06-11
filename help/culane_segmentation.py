import os
import shutil

'''
Script para dividir el dataset CULane en subdirectorios por escenario.
Este script asume que tienes un dataset CULane descargado y que los archivos de texto que indican las imágenes por escenario están en la estructura de carpetas correcta.

Estructura esperada:
- Las imágenes deben estar en subcarpetas tipo driver_XX_YYframe dentro de 'base_path'.
- Los archivos .txt deben estar en la ruta indicada (por ejemplo: list/test_split/test0_normal.txt).

Este script:
1. Crea una carpeta por cada escenario (normal, night, curve, etc.).
2. Lee las rutas relativas desde los .txt de cada escenario.
3. Copia las imágenes correspondientes desde el dataset original a su carpeta de escenario dentro de 'CULane_subset'.
4. Si una imagen no existe, simplemente la ignora sin lanzar error.

Puede usarse como base para construir subsets por tipo de escena, entrenar modelos específicos por condición o visualizar ejemplos concretos.
'''

# Ruta al dataset original.
base_path = "."

# Ruta destino donde guardarás las imágenes divididas por escenarios.
dest_path = "CULane_subset"

# Diccionario de txt por escenario.
scenario_files = {
    "normal": "list/test_split/test0_normal.txt",
    "crowd": "list/test_split/test1_crowd.txt",
    "hlight": "list/test_split/test2_hlight.txt",
    "shadow": "list/test_split/test3_shadow.txt",
    "noline": "list/test_split/test4_noline.txt",
    "arrow": "list/test_split/test5_arrow.txt",
    "curve": "list/test_split/test6_curve.txt",
    "cross": "list/test_split/test7_cross.txt",
    "night": "list/test_split/test8_night.txt"
}

for scenario, txt_file in scenario_files.items():
    with open(txt_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        rel_path = line.strip()
        src = os.path.join(base_path, rel_path)
        dst = os.path.join(dest_path, scenario, os.path.basename(rel_path))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"Copiado: {src} a {dst}")
        else:
            print(f"Falta: {src}")
