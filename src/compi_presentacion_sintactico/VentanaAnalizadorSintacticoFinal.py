import os
import sys

lib_path6 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintactico_analizadorLRFinal'))
sys.path.append(lib_path6)

from Analizador_Sintactico import analizadorSintacticoJava

def VentanaSintaktikoFinal():
    analizadorSintacticoJava
    
#analizadorSintacticoJava()