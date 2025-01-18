import os
import sys

lib_path4 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_TablaLR'))
sys.path.append(lib_path4)

from Tabla_Analizador_Sintacticov2 import InterfazTablaAS

def ventanaTablaSintactico():
    InterfazTablaAS()
    
#ventanaTablaSintactico()