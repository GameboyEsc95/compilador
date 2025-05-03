# semantico/a_semantico.py

from simbolos.t_simbolos import *  # Asegúrate de importar la tabla de símbolos
from semantico.err_semanticos import *  # Importa los errores semánticos si los tienes definidos
from lark import Tree

class AnalizadorSemantico:
    def __init__(self):
        self.simbolos = {}  # tabla de símbolos básica

    def analizar(self, arbol: Tree):
        self._analizar_nodo(arbol)

    def _analizar_nodo(self, nodo):
        if isinstance(nodo, Tree):
            if nodo.data == "declaracion_variable":
                tipo = nodo.children[0].value
                nombre = nodo.children[1].value
                if nombre in self.simbolos:
                    raise Exception(f"Variable '{nombre}' ya declarada")
                self.simbolos[nombre] = tipo
            elif nodo.data == "asignacion":
                nombre = nodo.children[0].value
                if nombre not in self.simbolos:
                    raise Exception(f"Variable '{nombre}' no declarada antes de usar")
            
            # Recursivo para todos los hijos
            for hijo in nodo.children:
                self._analizar_nodo(hijo)
