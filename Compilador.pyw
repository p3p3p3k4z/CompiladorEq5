import sys
import os

# Agregar la ruta a la carpeta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.VentanaPrincipal import *

ventanaPrincipal()
