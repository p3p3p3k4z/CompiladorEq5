import os
import sys

lib_path5 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintactico_analizadorLR'))
sys.path.append(lib_path5)

from analisisSintacticoLR import analisisSintactico

def ventanaSintaktiko():
    analisisSintactico()
    

#ventanaSintaktiko()