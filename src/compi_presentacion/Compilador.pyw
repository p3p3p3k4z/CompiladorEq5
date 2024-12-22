from VentanaPrincipal import ventanaPrincipal
from VentanaPrincipalAux import ventanaPrincipal_Aux

try:
    ventanaPrincipal()
except ImportError as e:
    print(f"Error de importación: {e}")
    ventanaPrincipal_Aux()
except RuntimeError as e:
    print(f"Error de ejecución: {e}")
    ventanaPrincipal_Aux()
except Exception as e:
    print(f"Otro error: {e}")
    ventanaPrincipal_Aux()
except SyntaxError as e:
    print(f"Error de sintaxis en VentanaPrincipal: {e}")
    ventanaPrincipal_Aux()
else:
	print("posible error?");
	#ventanaPrincipal_Aux()
