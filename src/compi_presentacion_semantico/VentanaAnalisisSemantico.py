import os
import sys

lib_path6 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_Analizador_Semantico'))
sys.path.append(lib_path6)

from analisis_semantico import analizadorSemantico

def VentanaSemantiko():
    analizadorSemantico()
    
#VentanaSemantiko()