import sys
from pathlib import Path

# Añade la carpeta 'src' al camino de búsqueda de módulos de Python
raiz_proyecto = Path(__file__).resolve().parent.parent
ruta_src = str(raiz_proyecto / "src")

if ruta_src not in sys.path:
    sys.path.insert(0, ruta_src)