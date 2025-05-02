from simbolos.t_simbolos import *
from err_semanticos import *

ts = TablaSimbolos()

# Agregar variable
var = Variable(nombre="x", tipo="int", ambito=0, linea_decl=1, tamanio_memoria=4)
ts.insertar(var)

# Buscar variable
resultado = ts.buscar("x")
if resultado:
    print(f"{resultado.nombre} fue declarado como {resultado.tipo}")


def verificar_suma(tipo1, tipo2, linea):
    if tipo1 != "int" or tipo2 != "int":
        raise ErrorTipoIncompatible("+", tipo1, tipo2, linea)